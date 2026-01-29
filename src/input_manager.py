import pyray as pr

# --- CONSTANTS ---
# Logical Actions (Strings are easier to debug than Enums)
ACTION_UP = "UP"
ACTION_DOWN = "DOWN"
ACTION_LEFT = "LEFT"
ACTION_RIGHT = "RIGHT"
ACTION_ACCEPT = "ACCEPT"
ACTION_BACK = "BACK"
ACTION_MENU = "MENU"

class InputBinding:
    """Represents a single physical input (Key, Button, or Stick Move)"""
    TYPE_KEY = "key"
    TYPE_BUTTON = "button"
    TYPE_AXIS = "axis"

    def __init__(self, kind, value, gamepad_id=0, axis_dir=0):
        self.kind = kind           # 'key', 'button', 'axis'
        self.value = value         # The Raylib KeyCode or ButtonCode
        self.gamepad_id = gamepad_id
        self.axis_dir = axis_dir   # 1 for Positive (Down/Right), -1 for Negative (Up/Left)

class InputManager:
    def __init__(self):
        self.bindings = {} # Dictionary: { "UP": [Binding1, Binding2], "DOWN": [...] }
        self._setup_defaults()

    def _setup_defaults(self):
        """Hardcoded defaults for now. Later, load this from DB."""        
        # --- UP ACTION ---
        self.bind(ACTION_UP, InputBinding(InputBinding.TYPE_KEY, pr.KeyboardKey.KEY_UP)) #265
        self.bind(ACTION_UP, InputBinding(InputBinding.TYPE_KEY, pr.KeyboardKey.KEY_W)) #87
        self.bind(ACTION_UP, InputBinding(InputBinding.TYPE_BUTTON, pr.GamepadButton.GAMEPAD_BUTTON_LEFT_FACE_UP, gamepad_id=0))
        self.bind(ACTION_UP, InputBinding(InputBinding.TYPE_AXIS, pr.GamepadAxis.GAMEPAD_AXIS_LEFT_Y, gamepad_id=0, axis_dir=-1))

        # --- DOWN ACTION ---
        self.bind(ACTION_DOWN, InputBinding(InputBinding.TYPE_KEY, pr.KeyboardKey.KEY_DOWN))
        self.bind(ACTION_DOWN, InputBinding(InputBinding.TYPE_KEY, pr.KeyboardKey.KEY_S))
        self.bind(ACTION_DOWN, InputBinding(InputBinding.TYPE_BUTTON, pr.GamepadButton.GAMEPAD_BUTTON_LEFT_FACE_DOWN, gamepad_id=0))
        self.bind(ACTION_DOWN, InputBinding(InputBinding.TYPE_AXIS, pr.GamepadAxis.GAMEPAD_AXIS_LEFT_Y, gamepad_id=0, axis_dir=1))

        # --- LEFT ACTION ---
        self.bind(ACTION_LEFT, InputBinding(InputBinding.TYPE_KEY, pr.KeyboardKey.KEY_LEFT))
        self.bind(ACTION_LEFT, InputBinding(InputBinding.TYPE_KEY, pr.KeyboardKey.KEY_A))

        # --- RIGHT ACTION ---
        self.bind(ACTION_RIGHT, InputBinding(InputBinding.TYPE_KEY, pr.KeyboardKey.KEY_RIGHT))
        self.bind(ACTION_RIGHT, InputBinding(InputBinding.TYPE_KEY, pr.KeyboardKey.KEY_D))                

        # --- ACCEPT ACTION ---
        self.bind(ACTION_ACCEPT, InputBinding(InputBinding.TYPE_KEY, pr.KeyboardKey.KEY_ENTER))
        self.bind(ACTION_ACCEPT, InputBinding(InputBinding.TYPE_BUTTON, pr.GamepadButton.GAMEPAD_BUTTON_RIGHT_FACE_DOWN, gamepad_id=0))

    def bind(self, action, binding):
        if action not in self.bindings:
            self.bindings[action] = []
        self.bindings[action].append(binding)
    
    def is_pressed(self, action):
        """Returns True if the action was JUST pressed this frame"""
        if action not in self.bindings: return False
        
        for bind in self.bindings[action]:
            if bind.kind == InputBinding.TYPE_KEY:
                if pr.is_key_pressed(bind.value): return True
            
            elif bind.kind == InputBinding.TYPE_BUTTON:
                if pr.is_gamepad_button_pressed(bind.gamepad_id, bind.value): return True
                
            elif bind.kind == InputBinding.TYPE_AXIS:
                # Axis "Pressed" is tricky. We treat it as a digital press 
                # if it wasn't held last frame (omitted for simplicity here, just checking value)
                val = pr.get_gamepad_axis_movement(bind.gamepad_id, bind.value)
                if bind.axis_dir == -1 and val < -0.5: return True
                if bind.axis_dir == 1 and val > 0.5: return True
        return False

    def is_held(self, action):
        """Returns True if the action is CURRENTLY held down"""
        if action not in self.bindings: return False
        
        for bind in self.bindings[action]:
            if bind.kind == InputBinding.TYPE_KEY:
                if pr.is_key_down(bind.value): return True
            
            elif bind.kind == InputBinding.TYPE_BUTTON:
                if pr.is_gamepad_button_down(bind.gamepad_id, bind.value): return True

            elif bind.kind == InputBinding.TYPE_AXIS:
                val = pr.get_gamepad_axis_movement(bind.gamepad_id, bind.value)
                if bind.axis_dir == -1 and val < -0.5: return True
                if bind.axis_dir == 1 and val > 0.5: return True
                
        return False