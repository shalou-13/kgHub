"""Feedback collection and logging module."""
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class FeedbackCollector:
    """Collects and stores user feedback for query results."""
    
    def __init__(self, feedback_file: str = "feedback_log.jsonl"):
        """Initialize feedback collector.
        
        Args:
            feedback_file: Path to feedback log file
        """
        self.feedback_file = Path(feedback_file)
        self.feedback_file.parent.mkdir(parents=True, exist_ok=True)
        
    def log_query(self, question: str, sql: str, 
                  success: bool, results: Optional[List[Dict]] = None,
                  error: Optional[str] = None,
                  feedback: Optional[str] = None,
                  corrected_sql: Optional[str] = None) -> str:
        """Log a query and its results.
        
        Args:
            question: Natural language question
            sql: Generated SQL query
            success: Whether execution was successful
            results: Query results (if successful)
            error: Error message (if failed)
            feedback: User feedback (correct/partial/wrong)
            corrected_sql: User-corrected SQL (if provided)
            
        Returns:
            Query ID
        """
        query_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        
        log_entry = {
            "query_id": query_id,
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "generated_sql": sql,
            "success": success,
            "result_count": len(results) if results else 0,
            "error": error,
            "feedback": feedback,
            "corrected_sql": corrected_sql
        }
        
        # Append to JSONL file
        with open(self.feedback_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        
        logger.info(f"Logged query {query_id}")
        return query_id
    
    def add_feedback(self, query_id: str, feedback: str, 
                    corrected_sql: Optional[str] = None):
        """Add feedback for a previously logged query.
        
        Args:
            query_id: Query ID to add feedback to
            feedback: Feedback label (correct/partial/wrong)
            corrected_sql: Corrected SQL if provided by user
        """
        # This is a simplified version that appends new feedback
        # In production, you might want to update the original entry
        feedback_entry = {
            "query_id": query_id,
            "timestamp": datetime.now().isoformat(),
            "feedback": feedback,
            "corrected_sql": corrected_sql,
            "feedback_update": True
        }
        
        with open(self.feedback_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(feedback_entry, ensure_ascii=False) + '\n')
        
        logger.info(f"Added feedback for query {query_id}: {feedback}")
    
    def get_feedback_stats(self) -> Dict:
        """Get statistics about collected feedback.
        
        Returns:
            Dictionary with feedback statistics
        """
        stats = {
            "total_queries": 0,
            "successful_queries": 0,
            "failed_queries": 0,
            "with_feedback": 0,
            "correct": 0,
            "partial": 0,
            "wrong": 0
        }
        
        if not self.feedback_file.exists():
            return stats
        
        with open(self.feedback_file, 'r', encoding='utf-8') as f:
            for line in f:
                entry = json.loads(line)
                
                # Skip feedback updates
                if entry.get("feedback_update"):
                    continue
                
                stats["total_queries"] += 1
                
                if entry.get("success"):
                    stats["successful_queries"] += 1
                else:
                    stats["failed_queries"] += 1
                
                feedback = entry.get("feedback")
                if feedback:
                    stats["with_feedback"] += 1
                    if feedback == "correct":
                        stats["correct"] += 1
                    elif feedback == "partial":
                        stats["partial"] += 1
                    elif feedback == "wrong":
                        stats["wrong"] += 1
        
        return stats
    
    def export_training_data(self, output_file: str, 
                            feedback_filter: Optional[List[str]] = None):
        """Export queries with feedback as training data.
        
        Args:
            output_file: Path to output file
            feedback_filter: List of feedback types to include (e.g., ["correct", "partial"])
        """
        if feedback_filter is None:
            feedback_filter = ["correct"]
        
        training_data = []
        
        if not self.feedback_file.exists():
            logger.warning("No feedback file found")
            return
        
        # Read all entries
        queries = {}
        with open(self.feedback_file, 'r', encoding='utf-8') as f:
            for line in f:
                entry = json.loads(line)
                query_id = entry.get("query_id")
                
                if entry.get("feedback_update"):
                    # Update existing entry with feedback
                    if query_id in queries:
                        queries[query_id]["feedback"] = entry.get("feedback")
                        queries[query_id]["corrected_sql"] = entry.get("corrected_sql")
                else:
                    queries[query_id] = entry
        
        # Filter and export
        for query_id, entry in queries.items():
            feedback = entry.get("feedback")
            
            if feedback in feedback_filter:
                # Use corrected SQL if available, otherwise use generated SQL
                sql = entry.get("corrected_sql") or entry.get("generated_sql")
                
                training_data.append({
                    "question": entry.get("question"),
                    "sql": sql
                })
        
        # Save to file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(training_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Exported {len(training_data)} training examples to {output_file}")
