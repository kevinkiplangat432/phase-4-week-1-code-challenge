from flask import Blueprint, request, jsonify
from flask_mail import Message
from app import db, mail
from app.models import Hero, Power, HeroPower

bp = Blueprint('api', __name__)

@bp.route('/')
def index():
    return jsonify({
        "message": "Welcome to Superheroes API",
        "endpoints": {
            "heroes": "/heroes",
            "powers": "/powers",
            "hero_powers": "/hero_powers"
        }
    })

@bp.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([hero.to_dict() for hero in heroes])

@bp.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({'error': 'Hero not found'}), 404
    
    return jsonify(hero.to_dict_with_powers())

@bp.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    return jsonify([power.to_dict() for power in powers])

@bp.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({'error': 'Power not found'}), 404
    
    return jsonify(power.to_dict())

@bp.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({'error': 'Power not found'}), 404
    
    data = request.get_json()
    if not data or 'description' not in data:
        return jsonify({'errors': ['Description is required']}), 400
    
    try:
        # Validate description length
        description = data['description']
        if not description or len(description) < 20:
            return jsonify({'errors': ['Description must be at least 20 characters long']}), 400
        
        power.description = description
        db.session.commit()
        return jsonify(power.to_dict())
    except ValueError as e:
        db.session.rollback()
        return jsonify({'errors': [str(e)]}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'errors': ['An error occurred while updating the power']}), 400

@bp.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    
    if not data:
        return jsonify({'errors': ['Request body is required']}), 400
    
    required_fields = ['strength', 'power_id', 'hero_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'errors': [f'{field} is required']}), 400
    
    # Check if hero and power exist
    hero = Hero.query.get(data['hero_id'])
    power = Power.query.get(data['power_id'])
    
    if not hero:
        return jsonify({'errors': ['Hero not found']}), 404
    if not power:
        return jsonify({'errors': ['Power not found']}), 404
    
    try:
        hero_power = HeroPower(
            strength=data['strength'],
            hero_id=data['hero_id'],
            power_id=data['power_id']
        )
        
        db.session.add(hero_power)
        db.session.commit()
        
        return jsonify(hero_power.to_dict()), 201
    except ValueError as e:
        db.session.rollback()
        return jsonify({'errors': [str(e)]}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'errors': ['An error occurred while creating the hero power']}), 400
    
@bp.route('/send-test-email', methods=['POST'])
def send_test_email():
    """Send a test email to verify email functionality"""
    data = request.get_json()
    
    if not data or 'to' not in data:
        return jsonify({'error': 'Recipient email is required'}), 400
    
    recipient = data['to']
    
    try:
        msg = Message(
            subject='Superheroes API Test Email',
            recipients=[recipient],
            body=f'''Hello from Superheroes API!

This is a test email to confirm that the Flask-Mail integration is working correctly.

If you received this email, the mail functionality is working properly!

Best regards,
Superheroes API Team
''',
            html=f'''<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #4CAF50; color: white; padding: 10px; text-align: center; }}
        .content {{ padding: 20px; }}
        .footer {{ margin-top: 20px; padding-top: 10px; border-top: 1px solid #eee; font-size: 12px; color: #666; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Superheroes API Test Email</h1>
        </div>
        <div class="content">
            <p>Hello from <strong>Superheroes API</strong>!</p>
            <p>This is a test email to confirm that the Flask-Mail integration is working correctly.</p>
            <p>If you received this email, the mail functionality is working properly!</p>
        </div>
        <div class="footer">
            <p>Best regards,<br>Superheroes API Team</p>
            <p>This is an automated message from the Superheroes API system.</p>
        </div>
    </div>
</body>
</html>'''
        )
        
        mail.send(msg)
        
        return jsonify({
            'message': f'Test email sent successfully to {recipient}',
            'status': 'success'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to send email',
            'details': str(e)
        }), 500

@bp.route('/notify-power-update', methods=['POST'])
def notify_power_update():
    """Send email notification when a power is updated"""
    data = request.get_json()
    
    if not data or 'power_id' not in data or 'email' not in data:
        return jsonify({'error': 'Power ID and recipient email are required'}), 400
    
    power_id = data['power_id']
    recipient_email = data['email']
    
    # Get the power
    power = Power.query.get(power_id)
    if not power:
        return jsonify({'error': 'Power not found'}), 404
    
    try:
        msg = Message(
            subject=f'Power Updated: {power.name}',
            recipients=[recipient_email],
            body=f'''Power Update Notification

Power Name: {power.name}
Power ID: {power.id}
Description: {power.description}

This power has been recently updated in the Superheroes API database.

You are receiving this notification because you subscribed to updates for this power.

Best regards,
Superheroes API System
''',
            html=f'''<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #2196F3; color: white; padding: 15px; text-align: center; }}
        .power-info {{ background-color: #f9f9f9; padding: 15px; margin: 15px 0; border-left: 4px solid #2196F3; }}
        .footer {{ margin-top: 20px; padding-top: 10px; border-top: 1px solid #eee; font-size: 12px; color: #666; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Power Update Notification</h1>
        </div>
        
        <p>Hello,</p>
        <p>A power has been updated in the Superheroes API database.</p>
        
        <div class="power-info">
            <h3>Power Details:</h3>
            <p><strong>Power Name:</strong> {power.name}</p>
            <p><strong>Power ID:</strong> {power.id}</p>
            <p><strong>Description:</strong> {power.description}</p>
        </div>
        
        <p>You are receiving this notification because you subscribed to updates for this power.</p>
        
        <div class="footer">
            <p>Best regards,<br><strong>Superheroes API System</strong></p>
            <p>This is an automated notification message.</p>
        </div>
    </div>
</body>
</html>'''
        )
        
        mail.send(msg)
        
        return jsonify({
            'message': f'Notification sent successfully for power: {power.name}',
            'power': power.to_dict(),
            'status': 'success'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to send notification email',
            'details': str(e)
        }), 500

@bp.route('/welcome-hero', methods=['POST'])
def welcome_new_hero():
    """Send welcome email when a new hero is added (simulated)"""
    data = request.get_json()
    
    if not data or 'hero_name' not in data or 'email' not in data:
        return jsonify({'error': 'Hero name and email are required'}), 400
    
    hero_name = data['hero_name']
    super_name = data.get('super_name', 'Unknown Hero')
    recipient_email = data['email']
    
    try:
        msg = Message(
            subject=f'Welcome to the Superheroes API, {hero_name}!',
            recipients=[recipient_email],
            body=f'''Welcome to Superheroes API!

Dear {hero_name} ({super_name}),

Welcome to the Superheroes API! Your profile has been successfully added to our database.

You are now part of our growing community of superheroes. You can:
1. View your profile at /heroes endpoint
2. Get associated with powers
3. Be discovered by fans worldwide

If you have any questions or need to update your information, please contact our admin team.

Stay heroic!

Best regards,
Superheroes API Team
''',
            html=f'''<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; border-radius: 5px; }}
        .welcome-message {{ padding: 20px; background-color: #f8f9fa; border-radius: 5px; margin: 20px 0; }}
        .features {{ margin: 20px 0; }}
        .feature {{ background: white; padding: 10px; margin: 10px 0; border-left: 4px solid #667eea; }}
        .footer {{ margin-top: 30px; padding-top: 20px; border-top: 2px solid #eee; text-align: center; color: #666; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Welcome to Superheroes API! </h1>
        </div>
        
        <div class="welcome-message">
            <h2>Dear <strong>{hero_name}</strong> (<em>{super_name}</em>),</h2>
            <p>Welcome to the Superheroes API! Your profile has been successfully added to our database.</p>
            <p>You are now part of our growing community of superheroes.</p>
        </div>
        
        <div class="features">
            <h3>Here's what you can do:</h3>
            <div class="feature">
                <strong>1. View Your Profile</strong>
                <p>Your profile is now available at the /heroes endpoint</p>
            </div>
            <div class="feature">
                <strong>2. Get Associated with Powers</strong>
                <p>You can now be associated with various superpowers</p>
            </div>
            <div class="feature">
                <strong>3. Be Discovered by Fans</strong>
                <p>Your hero profile is now accessible to fans worldwide</p>
            </div>
        </div>
        
        <p>If you have any questions or need to update your information, please contact our admin team.</p>
        
        <div class="footer">
            <p><strong>Stay heroic!</strong></p>
            <p>Best regards,<br>The Superheroes API Team</p>
            <p style="font-size: 11px; color: #999;">This is an automated welcome message.</p>
        </div>
    </div>
</body>
</html>'''
        )
        
        mail.send(msg)
        
        return jsonify({
            'message': f'Welcome email sent successfully to {hero_name}',
            'hero': {
                'name': hero_name,
                'super_name': super_name
            },
            'status': 'success'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to send welcome email',
            'details': str(e)
        }), 500