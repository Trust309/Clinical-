"""
NWLVH Clinical Supervision Chatbot Backend
A Flask-based chatbot server for clinical supervision assistance
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime
import re

app = Flask(__name__)
CORS(app)

class ClinicalSupervisionChatbot:
    """
    A chatbot specialized in clinical supervision guidance
    """

    def __init__(self):
        self.conversation_history = []
        self.knowledge_base = {
            'clinical_supervision': {
                'keywords': ['what is', 'define', 'clinical supervision', 'supervision', 'cs', 'about'],
                'response': """Clinical supervision is a formal process of professional support and learning that enables practitioners to develop knowledge and competence, assume responsibility for their own practice, and enhance patient protection and safety.

Key components include:
- Regular structured meetings between supervisor and supervisee
- Reflection on clinical practice
- Case discussion and consultation
- Professional development planning
- Performance evaluation and feedback
- Emotional support and wellness check

It's essential for maintaining high standards of care and supporting clinician wellbeing."""
            },
            'best_practices': {
                'keywords': ['best practice', 'guidelines', 'effective', 'how to supervise', 'tips'],
                'response': """Best practices for clinical supervision:

1. **Structure & Scheduling**
   - Regular scheduled sessions (weekly or bi-weekly)
   - Protected time without interruptions
   - Clear agenda setting

2. **Environment**
   - Confidential and safe space
   - Non-judgmental atmosphere
   - Trust-building focus

3. **Process**
   - Active listening and reflection
   - Constructive feedback
   - Goal setting and tracking
   - Case-based learning

4. **Documentation**
   - Record key discussions
   - Track progress and goals
   - Maintain confidentiality

5. **Professional Development**
   - Focus on both clinical skills and personal growth
   - Encourage self-reflection
   - Support evidence-based practice

6. **Relationship**
   - Establish clear boundaries
   - Cultural sensitivity
   - Collaborative approach
   - Regular evaluation of supervision process"""
            },
            'feedback': {
                'keywords': ['feedback', 'critique', 'evaluation', 'assessment', 'review'],
                'response': """Effective feedback in clinical supervision follows the SMART-F framework:

**S - Specific**: Be concrete about behaviors and situations
- Not: "You need to communicate better"
- Instead: "In the team meeting, providing more context about patient needs would help"

**M - Meaningful**: Connect to outcomes and professional growth
- Explain why the feedback matters

**A - Actionable**: Provide clear steps for improvement
- What can they do differently?
- What resources or support do they need?

**R - Respectful**: Delivered with empathy and support
- Focus on behavior, not personality
- Acknowledge strengths alongside areas for growth

**T - Timely**: Given soon after observation
- While details are fresh
- When there's time to discuss

**F - Follow-up**: Check progress and provide support
- Schedule follow-up discussions
- Celebrate improvements

Remember: Feedback is a gift for growth, not a weapon for criticism."""
            },
            'ethics': {
                'keywords': ['ethical', 'ethics', 'boundaries', 'confidentiality', 'dual relationship', 'professional'],
                'response': """Key ethical considerations in clinical supervision:

1. **Confidentiality**
   - Clear limits discussed upfront
   - Mandatory reporting obligations
   - Information sharing protocols

2. **Professional Boundaries**
   - Maintain appropriate supervisor-supervisee relationship
   - Avoid dual relationships (social, romantic, financial)
   - Be aware of power dynamics

3. **Competence**
   - Supervise only within your scope of practice
   - Seek consultation when needed
   - Ongoing professional development

4. **Informed Consent**
   - Clear explanation of supervision process
   - Rights and responsibilities
   - Evaluation criteria

5. **Cultural Competence**
   - Respect for diversity
   - Awareness of own biases
   - Culturally responsive practice

6. **Documentation**
   - Accurate and timely records
   - Secure storage
   - Professional standards

7. **Duty of Care**
   - Patient safety paramount
   - Duty to warn when appropriate
   - Quality of care monitoring

Always refer to your professional code of ethics and organizational policies."""
            },
            'models': {
                'keywords': ['model', 'framework', 'approach', 'theory', 'style'],
                'response': """Common clinical supervision models:

1. **Developmental Models** (e.g., Integrated Developmental Model)
   - Supervisees progress through stages
   - Supervision adapts to developmental level
   - Focus on autonomy development

2. **Process-Based Models** (e.g., Hawkins & Shohet's 7-Eyed Model)
   - Focus on supervision relationship
   - Multiple perspectives on practice
   - Parallel processes awareness

3. **Reflective Models** (e.g., Schön's Reflective Practice)
   - Critical reflection on action
   - Learning from experience
   - Self-awareness development

4. **Competency-Based Models**
   - Specific skills and competencies
   - Clear performance criteria
   - Evidence-based practice focus

5. **Social Role Models** (e.g., Bernard's Discrimination Model)
   - Teacher, counselor, consultant roles
   - Flexible role adoption
   - Focus on interventions and conceptualization

6. **Integrated/Eclectic Models**
   - Combine elements from multiple approaches
   - Tailored to context and needs
   - Flexibility and adaptability

Choose based on organizational context, supervisee needs, and your theoretical orientation."""
            },
            'challenges': {
                'keywords': ['challenge', 'difficult', 'problem', 'issue', 'struggle', 'concern'],
                'response': """Common challenges in clinical supervision and solutions:

**Challenge: Time Constraints**
Solution: Schedule regular sessions and protect that time as clinical priority

**Challenge: Supervisee Resistance**
Solution: Explore concerns openly, establish trust, clarify expectations

**Challenge: Performance Issues**
Solution: Address promptly with clear feedback, action plans, and support

**Challenge: Personality Conflicts**
Solution: Focus on professional goals, seek consultation, consider reassignment if severe

**Challenge: Boundary Violations**
Solution: Re-establish clear boundaries, review policies, document concerns

**Challenge: Cultural Differences**
Solution: Engage in cultural humility, seek training, ask questions respectfully

**Challenge: Skill Gaps in Supervisor**
Solution: Seek supervision of supervision, additional training, peer consultation

**Challenge: Emotional Burnout**
Solution: Address wellness, normalize struggles, adjust workload if possible

**Challenge: Documentation Burden**
Solution: Use templates, integrate into session, keep it concise

**Challenge: Remote Supervision**
Solution: Use secure technology, establish clear protocols, maintain connection

Remember: Seeking consultation or supervision of your supervision is a sign of professional strength, not weakness."""
            },
            'documentation': {
                'keywords': ['document', 'record', 'notes', 'paperwork', 'write'],
                'response': """Documentation in clinical supervision should include:

**Essential Elements:**
1. Date, time, and duration of session
2. Participants present
3. Topics and cases discussed
4. Clinical concerns addressed
5. Goals set and progress reviewed
6. Feedback provided
7. Action items and follow-up plans
8. Any safety or ethical concerns
9. Supervisee's signature (when applicable)

**Best Practices:**
- Document soon after session (while fresh)
- Be objective and specific
- Avoid jargon and assumptions
- Focus on behaviors and observations
- Note strengths and areas for development
- Keep records secure and confidential
- Follow organizational policies
- Consider legal and professional standards

**Purpose of Documentation:**
- Legal protection
- Quality assurance
- Professional development tracking
- Continuity of care
- Evaluation evidence
- Risk management

**Storage:**
- Secure, confidential location
- Follow retention policies
- Comply with data protection regulations
- Limit access to authorized personnel

Remember: If it isn't documented, it didn't happen (legally speaking)."""
            },
            'frequency': {
                'keywords': ['how often', 'frequency', 'schedule', 'regular', 'when'],
                'response': """Recommended supervision frequency:

**New/Entry-Level Practitioners:**
- Weekly sessions (60-90 minutes)
- More intensive support needed
- Focus on skill development and confidence

**Developing Practitioners:**
- Bi-weekly sessions (60 minutes)
- Balance support and autonomy
- Focus on complex cases and growth

**Experienced Practitioners:**
- Monthly sessions (45-60 minutes)
- Focus on consultation and renewal
- Address complex or challenging situations

**Crisis Situations:**
- More frequent as needed
- Immediate consultation available
- Additional support and monitoring

**Factors Influencing Frequency:**
- Regulatory requirements
- Organizational policies
- Complexity of caseload
- Supervisee experience and needs
- Available resources
- Performance concerns
- Learning goals

**Key Principle:**
Consistency is more important than duration. Regular, scheduled sessions are more effective than sporadic longer meetings.

**Flexibility:**
Be willing to adjust frequency based on changing needs, but maintain regular contact even with experienced staff."""
            },
            'group_supervision': {
                'keywords': ['group', 'team', 'peer', 'multiple'],
                'response': """Group clinical supervision offers unique benefits:

**Advantages:**
- Peer learning and support
- Multiple perspectives on cases
- Cost and time efficiency
- Reduced isolation
- Normalizes challenges
- Builds team cohesion

**Structure:**
- 4-8 participants ideal
- 90-120 minute sessions
- Regular schedule (bi-weekly or monthly)
- Clear ground rules and confidentiality
- Rotating case presentations

**Facilitator Role:**
- Ensure balanced participation
- Manage time and focus
- Maintain psychological safety
- Address group dynamics
- Connect themes and learning

**Best Practices:**
- Establish trust and safety early
- Use structured formats
- Balance support and challenge
- Encourage diverse perspectives
- Address conflicts promptly

**Limitations:**
- Less individual attention
- May not address personal issues
- Some reluctance to share
- Group dynamics can complicate

**Recommendation:**
Consider combining group supervision with periodic individual sessions for comprehensive support."""
            }
        }

    def get_response(self, user_message):
        """
        Generate a response based on the user message
        """
        message_lower = user_message.lower()

        # Check greetings
        if any(greeting in message_lower for greeting in ['hello', 'hi', 'hey', 'good morning', 'good afternoon']):
            return "Hello! I'm the NWLVH Clinical Supervision Assistant. How can I help you with clinical supervision today?"

        # Check thanks
        if any(thanks in message_lower for thanks in ['thank', 'thanks', 'appreciate']):
            return "You're very welcome! I'm here anytime you have questions about clinical supervision. Feel free to ask anything else!"

        # Check help request
        if 'help' in message_lower and len(message_lower.split()) < 5:
            return """I can help you with:

- Clinical supervision concepts and definitions
- Best practices and guidelines
- Providing effective feedback
- Ethical considerations
- Supervision models and frameworks
- Common challenges and solutions
- Documentation requirements
- Session frequency and structure
- Group supervision approaches

What would you like to know more about?"""

        # Search knowledge base
        for key, data in self.knowledge_base.items():
            for keyword in data['keywords']:
                if keyword in message_lower:
                    return data['response']

        # Default response
        return """That's an interesting question. While I specialize in clinical supervision topics, I may need more context to provide the most helpful response.

Could you rephrase your question or ask about a specific aspect such as:
- Supervision best practices
- Ethical considerations
- Feedback techniques
- Documentation requirements
- Common challenges
- Supervision models

I'm here to help!"""

    def add_to_history(self, role, message):
        """
        Add message to conversation history
        """
        self.conversation_history.append({
            'role': role,
            'message': message,
            'timestamp': datetime.now().isoformat()
        })

# Initialize chatbot
chatbot = ClinicalSupervisionChatbot()

# Ward data - sample clinical ward information
WARD_DATA = {
    'wards': [
        {
            'id': 'ward-001',
            'name': 'Acute Medical Unit',
            'department': 'Medicine',
            'capacity': 28,
            'current_occupancy': 24,
            'staff_on_duty': {
                'nurses': 6,
                'doctors': 2,
                'support_staff': 3
            },
            'specialties': ['General Medicine', 'Respiratory', 'Cardiology'],
            'contact': {
                'phone': '01234 567890',
                'extension': '2001'
            }
        },
        {
            'id': 'ward-002',
            'name': 'Surgical Ward A',
            'department': 'Surgery',
            'capacity': 32,
            'current_occupancy': 29,
            'staff_on_duty': {
                'nurses': 7,
                'doctors': 3,
                'support_staff': 4
            },
            'specialties': ['General Surgery', 'Orthopedics', 'Vascular'],
            'contact': {
                'phone': '01234 567891',
                'extension': '2002'
            }
        },
        {
            'id': 'ward-003',
            'name': 'Maternity Ward',
            'department': 'Obstetrics',
            'capacity': 20,
            'current_occupancy': 16,
            'staff_on_duty': {
                'midwives': 5,
                'nurses': 3,
                'doctors': 2,
                'support_staff': 2
            },
            'specialties': ['Maternity', 'Neonatal Care'],
            'contact': {
                'phone': '01234 567892',
                'extension': '2003'
            }
        },
        {
            'id': 'ward-004',
            'name': 'Pediatric Ward',
            'department': 'Pediatrics',
            'capacity': 24,
            'current_occupancy': 18,
            'staff_on_duty': {
                'nurses': 6,
                'doctors': 2,
                'support_staff': 3,
                'play_specialists': 2
            },
            'specialties': ['General Pediatrics', 'Pediatric Surgery'],
            'contact': {
                'phone': '01234 567893',
                'extension': '2004'
            }
        },
        {
            'id': 'ward-005',
            'name': 'Intensive Care Unit',
            'department': 'Critical Care',
            'capacity': 12,
            'current_occupancy': 10,
            'staff_on_duty': {
                'nurses': 12,
                'doctors': 4,
                'support_staff': 2
            },
            'specialties': ['Intensive Care', 'High Dependency'],
            'contact': {
                'phone': '01234 567894',
                'extension': '2005'
            }
        },
        {
            'id': 'ward-006',
            'name': 'Mental Health Unit',
            'department': 'Psychiatry',
            'capacity': 18,
            'current_occupancy': 14,
            'staff_on_duty': {
                'nurses': 5,
                'psychiatrists': 2,
                'psychologists': 1,
                'support_staff': 3
            },
            'specialties': ['Acute Psychiatry', 'Crisis Intervention'],
            'contact': {
                'phone': '01234 567895',
                'extension': '2006'
            }
        }
    ],
    'last_updated': datetime.now().isoformat()
}

@app.route('/')
def home():
    """
    Serve the chatbot interface
    """
    return """
    <html>
    <head><title>NWLVH Clinical Supervision Chatbot</title></head>
    <body>
        <h1>NWLVH Clinical Supervision Chatbot API</h1>
        <p>This is the backend API. Use the chatbot.html file for the interface.</p>
        <h2>Available Endpoints:</h2>
        <ul>
            <li>POST /chat - Send a message to the chatbot</li>
            <li>GET /history - Get conversation history</li>
            <li>POST /reset - Reset conversation</li>
            <li>GET /api/ward-data - Get all ward data</li>
            <li>GET /api/ward-data/&lt;ward_id&gt; - Get specific ward by ID</li>
        </ul>
    </body>
    </html>
    """

@app.route('/chat', methods=['POST'])
def chat():
    """
    Handle chat messages
    """
    try:
        data = request.get_json()
        user_message = data.get('message', '')

        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        # Add user message to history
        chatbot.add_to_history('user', user_message)

        # Get response
        bot_response = chatbot.get_response(user_message)

        # Add bot response to history
        chatbot.add_to_history('bot', bot_response)

        return jsonify({
            'response': bot_response,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history', methods=['GET'])
def get_history():
    """
    Get conversation history
    """
    return jsonify({
        'history': chatbot.conversation_history
    })

@app.route('/reset', methods=['POST'])
def reset():
    """
    Reset conversation history
    """
    chatbot.conversation_history = []
    return jsonify({
        'message': 'Conversation reset successfully'
    })

@app.route('/api/ward-data', methods=['GET'])
def get_ward_data():
    """
    Get ward data information
    Returns information about all clinical wards including capacity, staffing, and contact details
    """
    try:
        # Update timestamp to current time
        WARD_DATA['last_updated'] = datetime.now().isoformat()

        return jsonify(WARD_DATA), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to fetch ward data',
            'details': str(e)
        }), 500

@app.route('/api/ward-data/<ward_id>', methods=['GET'])
def get_ward_by_id(ward_id):
    """
    Get specific ward data by ID
    """
    try:
        # Find ward by ID
        ward = next((w for w in WARD_DATA['wards'] if w['id'] == ward_id), None)

        if ward:
            return jsonify({
                'ward': ward,
                'timestamp': datetime.now().isoformat()
            }), 200
        else:
            return jsonify({
                'error': 'Ward not found',
                'ward_id': ward_id
            }), 404

    except Exception as e:
        return jsonify({
            'error': 'Failed to fetch ward data',
            'details': str(e)
        }), 500

if __name__ == '__main__':
    print("Starting NWLVH Clinical Supervision Chatbot...")
    print("Access the API at http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
