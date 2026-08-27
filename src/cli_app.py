"""Command-line interface for NHP Claims Assessor."""

import argparse
import sys
from pathlib import Path
from src.config import Config, ReferenceData
from src.core.anaesthetic import calculate_modifier
from src.core.icd10 import ICDEngine
from src.core.workflow import WorkflowManager
from src.claims.models import Claim, ClaimFlag, FlagReason
from src.claims.processor import ClaimProcessor
from src.tracking.metrics import MetricsTracker
from src.chatbot.engine import ChatbotEngine
from src.export.excel import ExcelExporter


def calculate_modifier_cli(args):
    """CLI: Calculate anaesthetic modifier."""
    try:
        result = calculate_modifier(
            code=args.code,
            minutes=float(args.minutes),
            base_tariff=float(args.base_tariff),
            provider=args.provider,
        )
        print(f"\nModifier Calculation Result:")
        print(f"  Code: {result.code}")
        print(f"  Duration: {result.minutes} minutes")
        print(f"  Units: {result.units}")
        print(f"  Modifier Payment: N${result.modifier_payment}")
        print(f"  Total Claim Value: N${result.total_claim_value}\n")
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def search_icd10_cli(args):
    """CLI: Search ICD-10 codes."""
    engine = ICDEngine()
    results = engine.search(args.query, limit=int(args.limit))
    
    if results.empty:
        print("No results found.")
        return
    
    print(f"\nICD-10 Search Results for '{args.query}':")
    for _, row in results.iterrows():
        score = row.get('score', 'N/A')
        print(f"  {row['code']}: {row['description']} (score: {score})")
    print()


def workflow_cli(args):
    """CLI: Manage workflow."""
    manager = WorkflowManager()
    
    if args.action == 'status':
        status = manager.get_status()
        print(f"\nWorkflow Status: {status['progress']} complete ({status['percentage']:.1f}%)")
        for step in status['steps']:
            check = '✓' if step['completed'] else '○'
            print(f"  {check} {step['index'] + 1}. {step['name']}")
        print()
    
    elif args.action == 'complete':
        step_num = int(args.step) - 1
        manager.set_step(step_num, True)
        print(f"Step {step_num + 1} marked complete.")
    
    elif args.action == 'reset':
        manager.reset()
        print("Workflow reset to initial state.")


def chatbot_cli(args):
    """CLI: Interact with chatbot."""
    engine = ChatbotEngine()
    print(f"NHP Claims Chatbot (model: {engine.model})")
    print("Type 'exit' to quit.\n")
    
    step = int(args.step) if args.step else None
    
    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() == 'exit':
                print("Goodbye!")
                break
            if not user_input:
                continue
            
            response = engine.query(user_input, current_workflow_step=step)
            print(f"\nAssistant: {response['summary']}")
            if response['next_steps']:
                print("\nSuggested next steps:")
                for action in response['next_steps']:
                    print(f"  - {action}")
            print()
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)


def export_cli(args):
    """CLI: Export reference data."""
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    
    if args.type == 'icd10':
        engine = ICDEngine()
        df = engine.get_reference_data()
        df.to_csv(output, index=False)
        print(f"ICD-10 reference data exported to {output}")
    
    elif args.type == 'disciplines':
        excluded = list(ReferenceData.MK_EXCLUDED_DISCIPLINES)
        with open(output, 'w') as f:
            f.write('Excluded Disciplines (not MK eligible):\n')
            for disc in sorted(excluded):
                f.write(f"{disc}\n")
        print(f"Discipline list exported to {output}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='NHP Claims Assessor - Namibian Medical-Aid Claims Assessment Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python -m src.cli_app calculate 0036 45 1000.00
  python -m src.cli_app search "sinusitis"
  python -m src.cli_app workflow status
  python -m src.cli_app chatbot --step 2
        """,
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Calculate modifier
    calc_parser = subparsers.add_parser('calculate', help='Calculate anaesthetic modifier')
    calc_parser.add_argument('code', help='Modifier code (0036, 0023, 0038, 0039)')
    calc_parser.add_argument('minutes', help='Duration in minutes')
    calc_parser.add_argument('base_tariff', help='Base tariff in N$')
    calc_parser.add_argument('--provider', default='Anaesthetist', help='Provider type')
    calc_parser.set_defaults(func=calculate_modifier_cli)
    
    # Search ICD-10
    search_parser = subparsers.add_parser('search', help='Search ICD-10 codes')
    search_parser.add_argument('query', help='Search query (code or description)')
    search_parser.add_argument('--limit', default='8', help='Max results')
    search_parser.set_defaults(func=search_icd10_cli)
    
    # Workflow management
    workflow_parser = subparsers.add_parser('workflow', help='Manage workflow')
    workflow_parser.add_argument('action', choices=['status', 'complete', 'reset'])
    workflow_parser.add_argument('--step', help='Step number (for complete action)')
    workflow_parser.set_defaults(func=workflow_cli)
    
    # Chatbot interaction
    chat_parser = subparsers.add_parser('chatbot', help='Interact with chatbot')
    chat_parser.add_argument('--step', help='Current workflow step (0-6)')
    chat_parser.set_defaults(func=chatbot_cli)
    
    # Export data
    export_parser = subparsers.add_parser('export', help='Export reference data')
    export_parser.add_argument('type', choices=['icd10', 'disciplines'], help='Data type to export')
    export_parser.add_argument('output', help='Output file path')
    export_parser.set_defaults(func=export_cli)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    args.func(args)


if __name__ == '__main__':
    main()
