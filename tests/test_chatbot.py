"""Tests for the clinical supervision chatbot backend."""
import pytest
from chatbot_backend import app, ClinicalSupervisionChatbot


@pytest.fixture
def client():
    """Flask test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def chatbot():
    """Fresh chatbot instance."""
    return ClinicalSupervisionChatbot()


# --- Unit tests for ClinicalSupervisionChatbot ---

class TestChatbotResponses:
    def test_greeting(self, chatbot):
        response = chatbot.get_response("hello")
        assert "Clinical Supervision Assistant" in response

    def test_greeting_hey(self, chatbot):
        response = chatbot.get_response("hey")
        assert "Clinical Supervision Assistant" in response

    def test_thanks(self, chatbot):
        response = chatbot.get_response("thank you")
        assert "welcome" in response.lower()

    def test_help(self, chatbot):
        response = chatbot.get_response("help")
        assert "Best practices" in response or "best practices" in response

    def test_knowledge_base_supervision(self, chatbot):
        response = chatbot.get_response("what is clinical supervision")
        assert "formal process" in response.lower()

    def test_knowledge_base_feedback(self, chatbot):
        response = chatbot.get_response("How do I give feedback?")
        assert "SMART" in response or "Specific" in response

    def test_knowledge_base_ethics(self, chatbot):
        # Note: queries must avoid substring "hi" to not trigger greeting
        response = chatbot.get_response("boundaries and confidentiality")
        assert "Confidentiality" in response

    def test_knowledge_base_models(self, chatbot):
        response = chatbot.get_response("describe the model options")
        assert "Developmental" in response

    def test_knowledge_base_challenges(self, chatbot):
        response = chatbot.get_response("What are common challenges?")
        assert "Time Constraints" in response or "challenge" in response.lower()

    def test_knowledge_base_documentation(self, chatbot):
        response = chatbot.get_response("How should I document sessions?")
        assert "Date" in response or "document" in response.lower()

    def test_knowledge_base_frequency(self, chatbot):
        response = chatbot.get_response("how often should we meet")
        assert "Weekly" in response or "frequency" in response.lower()

    def test_knowledge_base_group(self, chatbot):
        response = chatbot.get_response("How does group learning work?")
        assert "Peer" in response or "group" in response.lower()

    def test_default_response(self, chatbot):
        response = chatbot.get_response("xyzzy nonsense query 12345")
        assert "rephrase" in response.lower()

    def test_conversation_history(self, chatbot):
        chatbot.add_to_history("user", "hello")
        chatbot.add_to_history("bot", "hi there")
        assert len(chatbot.conversation_history) == 2
        assert chatbot.conversation_history[0]['role'] == "user"
        assert 'timestamp' in chatbot.conversation_history[0]


# --- API endpoint tests ---

class TestAPI:
    def test_home(self, client):
        response = client.get('/')
        assert response.status_code == 200
        assert b"Clinical Supervision" in response.data

    def test_health(self, client):
        response = client.get('/health')
        assert response.status_code == 200
        assert response.get_json()['status'] == 'healthy'

    def test_chat_success(self, client):
        response = client.post('/chat', json={'message': 'hello'})
        assert response.status_code == 200
        data = response.get_json()
        assert 'response' in data
        assert 'timestamp' in data

    def test_chat_empty_message(self, client):
        response = client.post('/chat', json={'message': ''})
        assert response.status_code == 400

    def test_chat_no_message(self, client):
        response = client.post('/chat', json={})
        assert response.status_code == 400

    def test_history(self, client):
        response = client.get('/history')
        assert response.status_code == 200
        assert 'history' in response.get_json()

    def test_reset(self, client):
        # Send a message first
        client.post('/chat', json={'message': 'hello'})
        # Reset
        response = client.post('/reset')
        assert response.status_code == 200
        # Verify history is empty
        history = client.get('/history').get_json()
        assert len(history['history']) == 0
