"""
FlowFacilitator macOS Agent
Main entry point for the application
"""

import sys
import argparse
import logging
import signal
from pathlib import Path

from src.agent import FlowAgent
from src.config import load_config


def setup_logging(log_level: str, log_dir: Path):
    """Configure logging for the application"""
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "agent.log"
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )


def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    logging.info(f"Received signal {signum}, shutting down...")
    sys.exit(0)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='FlowFacilitator Agent')
    parser.add_argument('--dev', action='store_true', help='Run in development mode')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    parser.add_argument('--config', type=str, help='Path to config file')
    parser.add_argument('--ui', action='store_true', help='Launch with Mac UI')
    args = parser.parse_args()
    
    # If UI flag is set, launch the Mac UI
    if args.ui:
        from src.mac_ui import run_mac_ui
        run_mac_ui(dev_mode=args.dev)
        return
    
    # Load configuration
    config = load_config(args.config, dev_mode=args.dev)
    
    # Setup logging
    log_level = 'DEBUG' if args.debug else config['agent']['log_level']
    log_dir = Path.home() / 'Library' / 'Application Support' / 'FlowFacilitator' / 'logs'
    setup_logging(log_level, log_dir)
    
    logger = logging.getLogger(__name__)
    logger.info("Starting FlowFacilitator Agent...")
    logger.info(f"Development mode: {args.dev}")
    logger.info(f"Debug mode: {args.debug}")
    
    # Setup signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Create and start agent
        agent = FlowAgent(config)
        agent.start()
        
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down...")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
