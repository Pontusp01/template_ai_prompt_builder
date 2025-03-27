from flask import jsonify, request
import traceback
import sys

def register_color_routes(app, color_service):
    """Register color-related routes with the Flask app."""
    
    @app.route('/api/colors', methods=['GET'])
    def get_colors():
        try:
            print("GET /api/colors: Fetching colors")
            colors = color_service.get_all_colors()
            print(f"GET /api/colors: Retrieved {len(colors)} colors")
            return jsonify(colors)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error getting colors at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to retrieve colors', 'details': str(e)}), 500
    
    @app.route('/api/colors', methods=['POST'])
    def create_color():
        try:
            data = request.json
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            # Enhanced debug logging
            print(f"POST /api/colors: Received data: {data}")
            
            color = color_service.create_color(data)
            print(f"POST /api/colors: Created color with ID {color.get('id', 'unknown')} and hex_value {color.get('hex_value', 'unknown')}")
            
            return jsonify(color), 201
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error creating color at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to create color', 'details': str(e)}), 500
    
    @app.route('/api/colors/<color_id>', methods=['GET'])
    def get_color(color_id):
        try:
            # Get a single color
            colors = color_service.get_all_colors()
            color = next((c for c in colors if str(c['id']) == str(color_id)), None)
            
            if color:
                return jsonify(color)
            return jsonify({'error': 'Color not found'}), 404
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error getting color {color_id} at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to retrieve color', 'details': str(e)}), 500
    
    @app.route('/api/colors/<color_id>', methods=['PUT'])
    def update_color(color_id):
        try:
            data = request.json
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            # Enhanced debug logging
            print(f"PUT /api/colors/{color_id}: Received data: {data}")
            
            color = color_service.update_color(color_id, data)
            
            if color:
                print(f"PUT /api/colors/{color_id}: Updated color with hex_value {color.get('hex_value', 'unknown')}")
                return jsonify(color)
            return jsonify({'error': 'Color not found'}), 404
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error updating color {color_id} at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to update color', 'details': str(e)}), 500
    
    @app.route('/api/colors/<color_id>', methods=['DELETE'])
    def delete_color(color_id):
        try:
            success = color_service.delete_color(color_id)
            
            if success:
                return jsonify({'message': 'Color deleted'})
            return jsonify({'error': 'Color not found'}), 404
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = traceback.extract_tb(exc_tb)[-1][0]
            line = traceback.extract_tb(exc_tb)[-1][1]
            print(f"Error deleting color {color_id} at {fname}:{line}: {e}")
            print(f"Stacktrace: {traceback.format_exc()}")
            return jsonify({'error': 'Failed to delete color', 'details': str(e)}), 500