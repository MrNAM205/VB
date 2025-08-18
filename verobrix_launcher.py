import sys
import os
import json
from datetime import datetime

# Add modules to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'modules')))

from agents.JARVIS.jarvis_agent import extract_clauses, detect_contradictions, analyze_legal_structure
from agents.FRIDAY.friday_agent import interpret_tone, suggest_remedy, analyze_legal_risk, generate_legal_summary, log_provenance
from modules.remedy_synthesizer import RemedySynthesizer
from modules.situation_interpreter import SituationInterpreter

class VeroBrixSystem:
    """
    Enhanced VeroBrix system that integrates all modules for comprehensive legal analysis.
    """
    
    def __init__(self):
        self.remedy_synthesizer = RemedySynthesizer()
        self.situation_interpreter = SituationInterpreter()
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Ensure output directories exist
        os.makedirs("logs", exist_ok=True)
        os.makedirs("output", exist_ok=True)
        
        log_provenance("VeroBrix System", f"Initialized new session: {self.session_id}")
    
    def analyze_situation(self, input_text: str, situation_context: dict = None) -> dict:
        """
        Comprehensive analysis of a legal situation using all VeroBrix modules.
        
        Args:
            input_text: Raw text describing the legal situation
            situation_context: Optional additional context
            
        Returns:
            Complete analysis results
        """
        log_provenance("VeroBrix System", "Starting comprehensive situation analysis")
        
        # Step 1: Interpret the situation
        log_provenance("VeroBrix System", "Step 1: Interpreting situation with SituationInterpreter")
        situation = self.situation_interpreter.interpret_situation(input_text, situation_context)
        
        # Step 2: Extract clauses with JARVIS
        log_provenance("VeroBrix System", "Step 2: Extracting clauses with JARVIS")
        clauses = extract_clauses(input_text)
        
        # Step 3: Detect contradictions with JARVIS
        log_provenance("VeroBrix System", "Step 3: Detecting contradictions with JARVIS")
        contradictions = detect_contradictions(clauses)
        
        # Step 4: Analyze legal structure with JARVIS
        log_provenance("VeroBrix System", "Step 4: Analyzing legal structure with JARVIS")
        legal_structure = analyze_legal_structure(input_text)
        
        # Step 5: Analyze tone and risks with FRIDAY
        log_provenance("VeroBrix System", "Step 5: Analyzing tone and risks with FRIDAY")
        tone_analysis = interpret_tone(input_text)
        legal_risks = analyze_legal_risk(input_text)
        
        # Step 6: Generate legal summary with FRIDAY
        log_provenance("VeroBrix System", "Step 6: Generating legal summary with FRIDAY")
        legal_summary = generate_legal_summary(input_text, tone_analysis, legal_risks)
        
        # Step 7: Synthesize remedy
        log_provenance("VeroBrix System", "Step 7: Synthesizing remedy")
        remedy_input = {
            'type': situation['type'],
            'risk_level': legal_summary['risk_level'],
            'contradictions': contradictions,
            'tone_analysis': tone_analysis,
            'urgency': situation['urgency'],
            'jurisdiction': situation['jurisdiction'],
            'legal_framework': situation['legal_framework']
        }
        
        remedy = self.remedy_synthesizer.synthesize_remedy(remedy_input)
        
        # Compile comprehensive results
        results = {
            'session_id': self.session_id,
            'timestamp': datetime.now().isoformat(),
            'input': {
                'raw_text': input_text,
                'context': situation_context
            },
            'situation_analysis': situation,
            'legal_analysis': {
                'clauses': clauses,
                'contradictions': contradictions,
                'legal_structure': legal_structure,
                'tone_analysis': tone_analysis,
                'legal_risks': legal_risks,
                'legal_summary': legal_summary
            },
            'remedy': remedy,
            'recommendations': self._generate_recommendations(situation, legal_summary, remedy)
        }
        
        # Save results
        self._save_analysis_results(results)
        
        log_provenance("VeroBrix System", "Comprehensive analysis completed")
        return results
    
    def _generate_recommendations(self, situation: dict, legal_summary: dict, remedy: dict) -> dict:
        """Generate prioritized recommendations based on analysis."""
        recommendations = {
            'immediate_actions': [],
            'short_term_actions': [],
            'long_term_actions': [],
            'warnings': [],
            'opportunities': []
        }
        
        # Immediate actions based on urgency
        if situation['urgency']['level'] == 'high':
            recommendations['immediate_actions'].extend([
                'URGENT: Time-sensitive situation detected',
                'Review all deadlines and timelines immediately',
                'Consider emergency legal consultation'
            ])
        
        # Actions based on risk level
        if legal_summary['risk_level'] == 'HIGH':
            recommendations['immediate_actions'].append('HIGH RISK: Seek immediate legal counsel')
            recommendations['warnings'].append('Situation contains high-risk legal elements')
        
        # Actions based on contradictions
        if remedy.get('contradictions'):
            recommendations['short_term_actions'].append('Challenge contradictory provisions in documents')
        
        # Actions based on situation type
        situation_actions = {
            'traffic_stop': {
                'immediate': ['Document all details of the encounter', 'Preserve any evidence'],
                'short_term': ['Review citation for errors', 'Research applicable traffic laws'],
                'long_term': ['Consider challenging jurisdiction', 'File administrative remedy if applicable']
            },
            'fee_demand': {
                'immediate': ['Do not pay without challenging authority', 'Request fee schedule'],
                'short_term': ['Challenge lawful authority for fee', 'Demand due process hearing'],
                'long_term': ['File administrative appeal', 'Consider legal action if rights violated']
            },
            'court_summons': {
                'immediate': ['Calculate response deadline', 'Preserve all rights'],
                'short_term': ['File appropriate response', 'Challenge jurisdiction if applicable'],
                'long_term': ['Prepare defense strategy', 'Consider counterclaims if applicable']
            }
        }
        
        if situation['type'] in situation_actions:
            actions = situation_actions[situation['type']]
            recommendations['immediate_actions'].extend(actions.get('immediate', []))
            recommendations['short_term_actions'].extend(actions.get('short_term', []))
            recommendations['long_term_actions'].extend(actions.get('long_term', []))
        
        # Identify opportunities
        if legal_summary['tone_summary'] == 'positive':
            recommendations['opportunities'].append('Document contains favorable language - preserve these terms')
        
        if situation['jurisdiction']['primary'] == 'commercial':
            recommendations['opportunities'].append('Commercial jurisdiction may provide UCC protections')
        
        return recommendations
    
    def _save_analysis_results(self, results: dict):
        """Save analysis results to file."""
        filename = f"output/verobrix_analysis_{self.session_id}.json"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            log_provenance("VeroBrix System", f"Analysis results saved to {filename}")
        except Exception as e:
            log_provenance("VeroBrix System", f"Error saving results: {e}")
    
    def generate_document(self, template_name: str, variables: dict) -> str:
        """Generate a legal document using the remedy synthesizer."""
        log_provenance("VeroBrix System", f"Generating document: {template_name}")
        return self.remedy_synthesizer.generate_document(template_name, variables)
    
    def get_available_templates(self) -> list:
        """Get list of available document templates."""
        return self.remedy_synthesizer.get_available_templates()
    
    def print_analysis_summary(self, results: dict):
        """Print a formatted summary of the analysis results."""
        print("\n" + "="*60)
        print("VEROBRIX LEGAL ANALYSIS SUMMARY")
        print("="*60)
        
        # Basic information
        print(f"Session ID: {results['session_id']}")
        print(f"Analysis Time: {results['timestamp']}")
        print(f"Situation Type: {results['situation_analysis']['type'].upper()}")
        print(f"Risk Level: {results['legal_analysis']['legal_summary']['risk_level']}")
        print(f"Urgency: {results['situation_analysis']['urgency']['level'].upper()}")
        
        # Jurisdiction
        jurisdiction = results['situation_analysis']['jurisdiction']
        print(f"Primary Jurisdiction: {jurisdiction['primary'].upper()}")
        if jurisdiction['secondary']:
            print(f"Secondary Jurisdictions: {', '.join(jurisdiction['secondary']).upper()}")
        
        # Key entities
        entities = results['situation_analysis']['entities']
        if entities['people']:
            print(f"People Involved: {', '.join(entities['people'])}")
        if entities['organizations']:
            print(f"Organizations: {', '.join(entities['organizations'])}")
        
        # Contradictions
        contradictions = results['legal_analysis']['contradictions']
        if contradictions:
            print(f"\nCONTRADICTIONS DETECTED: {len(contradictions)}")
            for i, contradiction in enumerate(contradictions, 1):
                if isinstance(contradiction, dict):
                    print(f"  {i}. {contradiction.get('description', 'Unknown contradiction')}")
                else:
                    print(f"  {i}. {contradiction}")
        
        # Legal risks
        risks = results['legal_analysis']['legal_risks']
        if risks:
            print(f"\nLEGAL RISKS IDENTIFIED: {len(risks)}")
            for risk in risks:
                print(f"  - {risk['level']} RISK: {risk['description']}")
        
        # Immediate recommendations
        immediate = results['recommendations']['immediate_actions']
        if immediate:
            print(f"\nIMMEDIATE ACTIONS REQUIRED:")
            for action in immediate:
                print(f"  • {action}")
        
        # Warnings
        warnings = results['recommendations']['warnings']
        if warnings:
            print(f"\nWARNINGS:")
            for warning in warnings:
                print(f"  ⚠️  {warning}")
        
        # Legal strategies
        strategies = results['remedy']['legal_strategies']
        if strategies:
            print(f"\nRECOMMENDED LEGAL STRATEGIES:")
            for strategy in strategies:
                print(f"  • {strategy}")
        
        print("\n" + "="*60)

def main():
    """
    Enhanced main function with comprehensive legal analysis.
    """
    system = VeroBrixSystem()
    
    # Load input document
    try:
        with open("intake/sample_document.txt", "r", encoding='utf-8') as f:
            input_text = f.read()
        log_provenance("VeroBrix System", "Successfully loaded 'intake/sample_document.txt'")
    except FileNotFoundError:
        log_provenance("VeroBrix System", "Error: 'intake/sample_document.txt' not found")
        print("Please create the file 'intake/sample_document.txt' with some text.")
        return
    except Exception as e:
        log_provenance("VeroBrix System", f"Error loading input file: {e}")
        return
    
    # Perform comprehensive analysis
    try:
        results = system.analyze_situation(input_text)
        
        # Print summary
        system.print_analysis_summary(results)
        
        # Demonstrate document generation
        print("\n" + "="*60)
        print("DOCUMENT GENERATION EXAMPLE")
        print("="*60)
        
        # Generate a sample notice
        variables = {
            'OFFICER': 'Officer Johnson',
            'AGENCY': 'State Highway Patrol',
            'INDIVIDUAL_NAME': 'John Doe',
            'NAME': 'John Doe'
        }
        
        document = system.generate_document('traffic_stop', variables)
        print("Generated Notice of Lawful Travel:")
        print("-" * 40)
        print(document)
        
        print(f"\nFull analysis results saved to: output/verobrix_analysis_{system.session_id}.json")
        
    except Exception as e:
        log_provenance("VeroBrix System", f"Error during analysis: {e}")
        print(f"An error occurred during analysis: {e}")

if __name__ == "__main__":
    main()
