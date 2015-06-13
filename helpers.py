import math
import pygame
from pygame.locals import *

class Vector2:
    @staticmethod
    def zero():
        return Vector2(0, 0)

    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)

    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        else:
            return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
        else:
            return NotImplemented

    def __mul__(self, scalar):
        if type(scalar) in [int, float]:
            return Vector2(self.x * scalar, self.y * scalar)
        else:
            return NotImplemented

    def __iadd__(self, other):
        if isinstance(other, Vector2):
            self.x += other.x
            self.y += other.y

            return self
        else:
            return NotImplemented

    def __isub__(self, other):
        if isinstance(other, Vector2):
            self.x -= other.x
            self.y -= other.y

            return self
        else:
            return NotImplemented

    def __imul__(self, scalar):
        if type(scalar) in [int, float]:
            self.x *= scalar
            self.y *= scalar

            return self
        else:
            return NotImplemented

    @staticmethod
    def distance(v1, v2):
        deltax = v2.x - v1.x
        deltay = v2.y - v1.y

        return math.sqrt((deltax * deltax) + (deltay * deltay))

    def magnitude(self):
        return math.sqrt((self.x * self.x) + (self.y * self.y))

    def normalized(self):
        length = float(self.magnitude())
        if not length:
            return Vector2.zero()

        return Vector2(self.x / length, self.y / length)

    def __str__(self):
        return "({}, {})".format(self.x, self.y)


class Constants:
    sqrt2 = math.sqrt(2)
    MAXPLAYERSPEED = 2.6
    MAXENEMYSPEED = MAXPLAYERSPEED / 1.1

class Key:
    def __init__(self, keycode):
        self.keycode = keycode
        self.prevstate = 0
        self.pressed = False
        self.pressedReleased = False

    def update(self, state):
        if not self.prevstate and state:
            self.pressed = True
        elif self.prevstate and not state:
            self.pressedReleased = True
            self.pressed = False
        else:
            self.pressed = bool(state)
            self.pressedReleased = False
        self.prevstate = state

class Keys:
    mapping = [
            K_BACKSPACE,
            K_TAB,
            K_CLEAR,
            K_RETURN,
            K_PAUSE,
            K_ESCAPE,
            K_SPACE,
            K_EXCLAIM,
            K_QUOTEDBL,
            K_HASH,
            K_DOLLAR,
            K_AMPERSAND,
            K_QUOTE,
            K_LEFTPAREN,
            K_RIGHTPAREN,
            K_ASTERISK,
            K_PLUS,
            K_COMMA,
            K_MINUS,
            K_PERIOD,
            K_SLASH,
            K_0,
            K_1,
            K_2,
            K_3,
            K_4,
            K_5,
            K_6,
            K_7,
            K_8,
            K_9,
            K_COLON,
            K_SEMICOLON,
            K_LESS,
            K_EQUALS,
            K_GREATER,
            K_QUESTION,
            K_AT,
            K_LEFTBRACKET,
            K_BACKSLASH,
            K_RIGHTBRACKET,
            K_CARET,
            K_UNDERSCORE,
            K_BACKQUOTE,
            K_a,
            K_b,
            K_c,
            K_d,
            K_e,
            K_f,
            K_g,
            K_h,
            K_i,
            K_j,
            K_k,
            K_l,
            K_m,
            K_n,
            K_o,
            K_p,
            K_q,
            K_r,
            K_s,
            K_t,
            K_u,
            K_v,
            K_w,
            K_x,
            K_y,
            K_z,
            K_DELETE,
            K_KP0,
            K_KP1,
            K_KP2,
            K_KP3,
            K_KP4,
            K_KP5,
            K_KP6,
            K_KP7,
            K_KP8,
            K_KP9,
            K_KP_PERIOD,
            K_KP_DIVIDE,
            K_KP_MULTIPLY,
            K_KP_MINUS,
            K_KP_PLUS,
            K_KP_ENTER,
            K_KP_EQUALS,
            K_UP,
            K_DOWN,
            K_RIGHT,
            K_LEFT,
            K_INSERT,
            K_HOME,
            K_END,
            K_PAGEUP,
            K_PAGEDOWN,
            K_F1,
            K_F2,
            K_F3,
            K_F4,
            K_F5,
            K_F6,
            K_F7,
            K_F8,
            K_F9,
            K_F10,
            K_F11,
            K_F12,
            K_F13,
            K_F14,
            K_F15,
            K_NUMLOCK,
            K_CAPSLOCK,
            K_SCROLLOCK,
            K_RSHIFT,
            K_LSHIFT,
            K_RCTRL,
            K_LCTRL,
            K_RALT,
            K_LALT,
            K_RMETA,
            K_LMETA,
            K_LSUPER,
            K_RSUPER,
            K_MODE,
            K_HELP,
            K_PRINT,
            K_SYSREQ,
            K_BREAK,
            K_MENU,
            K_POWER,
            K_EURO
        ]
    keys = {
            K_BACKSPACE: Key(K_BACKSPACE),
            K_TAB: Key(K_TAB),
            K_CLEAR: Key(K_CLEAR),
            K_RETURN: Key(K_RETURN),
            K_PAUSE: Key(K_PAUSE),
            K_ESCAPE: Key(K_ESCAPE),
            K_SPACE: Key(K_SPACE),
            K_EXCLAIM: Key(K_EXCLAIM),
            K_QUOTEDBL: Key(K_QUOTEDBL),
            K_HASH: Key(K_HASH),
            K_DOLLAR: Key(K_DOLLAR),
            K_AMPERSAND: Key(K_AMPERSAND),
            K_QUOTE: Key(K_QUOTE),
            K_LEFTPAREN: Key(K_LEFTPAREN),
            K_RIGHTPAREN: Key(K_RIGHTPAREN),
            K_ASTERISK: Key(K_ASTERISK),
            K_PLUS: Key(K_PLUS),
            K_COMMA: Key(K_COMMA),
            K_MINUS: Key(K_MINUS),
            K_PERIOD: Key(K_PERIOD),
            K_SLASH: Key(K_SLASH),
            K_0: Key(K_0),
            K_1: Key(K_1),
            K_2: Key(K_2),
            K_3: Key(K_3),
            K_4: Key(K_4),
            K_5: Key(K_5),
            K_6: Key(K_6),
            K_7: Key(K_7),
            K_8: Key(K_8),
            K_9: Key(K_9),
            K_COLON: Key(K_COLON),
            K_SEMICOLON: Key(K_SEMICOLON),
            K_LESS: Key(K_LESS),
            K_EQUALS: Key(K_EQUALS),
            K_GREATER: Key(K_GREATER),
            K_QUESTION: Key(K_QUESTION),
            K_AT: Key(K_AT),
            K_LEFTBRACKET: Key(K_LEFTBRACKET),
            K_BACKSLASH: Key(K_BACKSLASH),
            K_RIGHTBRACKET: Key(K_RIGHTBRACKET),
            K_CARET: Key(K_CARET),
            K_UNDERSCORE: Key(K_UNDERSCORE),
            K_BACKQUOTE: Key(K_BACKQUOTE),
            K_a: Key(K_a),
            K_b: Key(K_b),
            K_c: Key(K_c),
            K_d: Key(K_d),
            K_e: Key(K_e),
            K_f: Key(K_f),
            K_g: Key(K_g),
            K_h: Key(K_h),
            K_i: Key(K_i),
            K_j: Key(K_j),
            K_k: Key(K_k),
            K_l: Key(K_l),
            K_m: Key(K_m),
            K_n: Key(K_n),
            K_o: Key(K_o),
            K_p: Key(K_p),
            K_q: Key(K_q),
            K_r: Key(K_r),
            K_s: Key(K_s),
            K_t: Key(K_t),
            K_u: Key(K_u),
            K_v: Key(K_v),
            K_w: Key(K_w),
            K_x: Key(K_x),
            K_y: Key(K_y),
            K_z: Key(K_z),
            K_DELETE: Key(K_DELETE),
            K_KP0: Key(K_KP0),
            K_KP1: Key(K_KP1),
            K_KP2: Key(K_KP2),
            K_KP3: Key(K_KP3),
            K_KP4: Key(K_KP4),
            K_KP5: Key(K_KP5),
            K_KP6: Key(K_KP6),
            K_KP7: Key(K_KP7),
            K_KP8: Key(K_KP8),
            K_KP9: Key(K_KP9),
            K_KP_PERIOD: Key(K_KP_PERIOD),
            K_KP_DIVIDE: Key(K_KP_DIVIDE),
            K_KP_MULTIPLY: Key(K_KP_MULTIPLY),
            K_KP_MINUS: Key(K_KP_MINUS),
            K_KP_PLUS: Key(K_KP_PLUS),
            K_KP_ENTER: Key(K_KP_ENTER),
            K_KP_EQUALS: Key(K_KP_EQUALS),
            K_UP: Key(K_UP),
            K_DOWN: Key(K_DOWN),
            K_RIGHT: Key(K_RIGHT),
            K_LEFT: Key(K_LEFT),
            K_INSERT: Key(K_INSERT),
            K_HOME: Key(K_HOME),
            K_END: Key(K_END),
            K_PAGEUP: Key(K_PAGEUP),
            K_PAGEDOWN: Key(K_PAGEDOWN),
            K_F1: Key(K_F1),
            K_F2: Key(K_F2),
            K_F3: Key(K_F3),
            K_F4: Key(K_F4),
            K_F5: Key(K_F5),
            K_F6: Key(K_F6),
            K_F7: Key(K_F7),
            K_F8: Key(K_F8),
            K_F9: Key(K_F9),
            K_F10: Key(K_F10),
            K_F11: Key(K_F11),
            K_F12: Key(K_F12),
            K_F13: Key(K_F13),
            K_F14: Key(K_F14),
            K_F15: Key(K_F15),
            K_NUMLOCK: Key(K_NUMLOCK),
            K_CAPSLOCK: Key(K_CAPSLOCK),
            K_SCROLLOCK: Key(K_SCROLLOCK),
            K_RSHIFT: Key(K_RSHIFT),
            K_LSHIFT: Key(K_LSHIFT),
            K_RCTRL: Key(K_RCTRL),
            K_LCTRL: Key(K_LCTRL),
            K_RALT: Key(K_RALT),
            K_LALT: Key(K_LALT),
            K_RMETA: Key(K_RMETA),
            K_LMETA: Key(K_LMETA),
            K_LSUPER: Key(K_LSUPER),
            K_RSUPER: Key(K_RSUPER),
            K_MODE: Key(K_MODE),
            K_HELP: Key(K_HELP),
            K_PRINT: Key(K_PRINT),
            K_SYSREQ: Key(K_SYSREQ),
            K_BREAK: Key(K_BREAK),
            K_MENU: Key(K_MENU),
            K_POWER: Key(K_POWER),
            K_EURO: Key(K_EURO)
        }

    @staticmethod
    def update():
        keystate = pygame.key.get_pressed()
        for (key, state) in enumerate(keystate):
            if key >= len(Keys.mapping):
                return
            Keys.keys[Keys.mapping[key]].update(state)

    @staticmethod
    def pressed(keyId):
        if keyId >= len(Keys.mapping): return None

        return Keys.keys[Keys.mapping[keyId]].pressed

    @staticmethod
    def get(keyId):
        if keyId >= len(Keys.mapping): return None

        return Keys.keys[Keys.mapping[keyId]]

class Mouse:
    leftClicked = False
    buttons = None
    prevStates = None
    pos = Vector2.zero()

    @staticmethod
    def update():
        Mouse.buttons = pygame.mouse.get_pressed()
        
        Mouse.leftClicked = False
        if Mouse.prevStates and Mouse.prevStates[0] and not Mouse.buttons[0]:
            Mouse.leftClicked = True

        mpos = pygame.mouse.get_pos()
        Mouse.pos = Vector2(mpos[0], mpos[1])

        Mouse.prevStates = Mouse.buttons