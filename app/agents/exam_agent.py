# app/agents/exam_agent.py
from typing import List, Dict, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod
from crewai import Agent, Task, Crew
from llm.llm_client import get_crewai_llm
from tools.pdf_chunk_loader import create_pdf_chunking_service, ChunkingConfig
from services.text_processor import TextProcessorService, get_text_processor

@dataclass
class ExamAnalysisRequest:
    """Data class for exam analysis requests"""
    exam_file_path: str
    study_material_paths: List[str]
    chat_id: str

@dataclass
class ExamAnalysisResult:
    """Data class for exam analysis results"""
    extracted_topics: List[str]
    study_recommendations: Dict[str, str]
    coverage_analysis: str
    preparation_suggestions: str

class ExamAnalyzer(ABC):
    """Abstract base class for exam analysis strategies"""
    
    @abstractmethod
    def analyze_exam_content(self, content: str) -> List[str]:
        pass
    
    @abstractmethod
    def analyze_study_coverage(self, exam_topics: List[str], study_content: str) -> Dict[str, str]:
        pass

class LLMExamAnalyzer(ExamAnalyzer):
    """Concrete implementation using LLM for exam analysis"""
    
    def __init__(self, text_processor: TextProcessorService):
        self.text_processor = text_processor
        self.llm = get_crewai_llm()  # Use CrewAI-compatible LLM
    
    def analyze_exam_content(self, content: str) -> List[str]:
        """Extract topics and themes from exam content"""
        from langchain.prompts import ChatPromptTemplate
        
        prompt = ChatPromptTemplate.from_template("""
        You are an academic exam analyzer. Analyze the following exam content and extract:
        - Main topics and subjects covered
        - Key concepts that students need to know
        - Skills and knowledge areas being tested
        
        Return a comma-separated list of topics.
        
        EXAM CONTENT:
        {content}
        """)
        
        result = self.llm.invoke(prompt.format(content=content))
        # Parse the comma-separated result into a list
        return [topic.strip() for topic in result.split(',') if topic.strip()]
    
    def analyze_study_coverage(self, exam_topics: List[str], study_content: str) -> Dict[str, str]:
        """Analyze how well study materials cover exam topics"""
        from langchain.prompts import ChatPromptTemplate
        
        topics_str = ", ".join(exam_topics)
        prompt = ChatPromptTemplate.from_template("""
        You are an academic study advisor. Given the following exam topics and study material content:
        
        EXAM TOPICS: {topics}
        STUDY CONTENT: {content}
        
        For each exam topic, analyze:
        1. How well the study material covers it (Well Covered/Partially Covered/Not Covered)
        2. What specific areas need more attention
        3. Recommendations for improvement
        
        Format your response as: Topic: Coverage_Status - Recommendations
        """)
        
        result = self.llm.invoke(prompt.format(topics=topics_str, content=study_content))
        
        # Parse the result into a dictionary
        coverage_dict = {}
        for line in result.split('\n'):
            if ':' in line and '-' in line:
                topic_part, recommendation = line.split('-', 1)
                topic = topic_part.split(':')[0].strip()
                coverage_dict[topic] = recommendation.strip()
        
        return coverage_dict

class ExamAgent:
    """Main exam agent that orchestrates the analysis process"""
    
    def __init__(self, analyzer: ExamAnalyzer, chunking_service=None):
        self.analyzer = analyzer
        self.chunking_service = chunking_service or create_pdf_chunking_service()
        self.llm = get_crewai_llm()  # Use CrewAI-compatible LLM
        self.agent = self._create_agent()
    
    def _create_agent(self) -> Agent:
        """Create the CrewAI agent for exam analysis"""
        return Agent(
            role='Academic Exam Advisor',
            goal='Analyze exam papers and provide study recommendations based on study materials',
            backstory=(
                "You are an expert academic advisor who helps students prepare for exams. "
                "You analyze exam content to identify key topics and assess study material coverage."
            ),
            allow_delegation=False,
            verbose=True,
            llm=self.llm
        )
    
    def _extract_content_from_files(self, file_paths: List[str]) -> str:
        """Extract and combine content from multiple files"""
        all_content = []
        for file_path in file_paths:
            try:
                chunks = self.chunking_service.extract_and_chunk(file_path)
                all_content.extend(chunks)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
        return "\n\n".join(all_content)
    
    def _create_analysis_task(self, request: ExamAnalysisRequest, analysis_result: ExamAnalysisResult) -> Task:
        """Create a comprehensive analysis task"""
        return Task(
            description=f"""
            Provide comprehensive exam preparation advice based on the analysis:
            
            EXAM TOPICS IDENTIFIED: {', '.join(analysis_result.extracted_topics)}
            COVERAGE ANALYSIS: {analysis_result.coverage_analysis}
            
            Provide:
            1. A study plan prioritizing weak areas
            2. Specific recommendations for each topic
            3. Time allocation suggestions
            4. Additional resources if needed
            """,
            expected_output="Comprehensive exam preparation strategy with actionable recommendations",
            agent=self.agent
        )
    
    def analyze_exam_and_materials(self, request: ExamAnalysisRequest) -> ExamAnalysisResult:
        """Main method to analyze exam and study materials"""
        # Extract content from exam file
        exam_content = self._extract_content_from_files([request.exam_file_path])
        
        # Extract content from study materials
        study_content = self._extract_content_from_files(request.study_material_paths)
        
        # Analyze exam content
        exam_topics = self.analyzer.analyze_exam_content(exam_content)
        
        # Analyze study coverage
        coverage_analysis = self.analyzer.analyze_study_coverage(exam_topics, study_content)
        
        # Create result object
        result = ExamAnalysisResult(
            extracted_topics=exam_topics,
            study_recommendations=coverage_analysis,
            coverage_analysis=str(coverage_analysis),
            preparation_suggestions=""
        )
        
        # Create and execute comprehensive analysis task
        task = self._create_analysis_task(request, result)
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            verbose=True
        )
        
        comprehensive_analysis = crew.kickoff()
        result.preparation_suggestions = str(comprehensive_analysis)
        
        return result

class ExamAgentService:
    """Service class for managing exam agent operations"""
    
    def __init__(self, analyzer: Optional[ExamAnalyzer] = None):
        if analyzer is None:
            text_processor = get_text_processor()
            analyzer = LLMExamAnalyzer(text_processor)
        
        self.exam_agent = ExamAgent(analyzer)
    
    def analyze_exam_preparation(self, 
                               exam_file_path: str, 
                               study_material_paths: List[str], 
                               chat_id: str) -> ExamAnalysisResult:
        """Convenience method for exam analysis"""
        request = ExamAnalysisRequest(
            exam_file_path=exam_file_path,
            study_material_paths=study_material_paths,
            chat_id=chat_id
        )
        return self.exam_agent.analyze_exam_and_materials(request)

# Factory function
def create_exam_agent_service() -> ExamAgentService:
    """Create an exam agent service with default configuration"""
    return ExamAgentService()

# Legacy function for backward compatibility
def analyze_exam_and_materials(exam_file_path: str, study_material_paths: List[str], chat_id: str) -> Dict:
    """Legacy function for backward compatibility"""
    service = create_exam_agent_service()
    result = service.analyze_exam_preparation(exam_file_path, study_material_paths, chat_id)
    
    return {
        "topics": result.extracted_topics,
        "coverage": result.study_recommendations,
        "recommendations": result.preparation_suggestions
    }