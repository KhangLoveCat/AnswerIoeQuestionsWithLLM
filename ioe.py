import keyboard
import pyautogui
import pytesseract
import ollama
from typing import Dict, Tuple

# Configure Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Constants
BUTTON_COORDS = {1: (0.23, 0.65), 2: (0.77, 0.65), 3: (0.20, 0.80), 4: (0.87, 0.80)}
REGIONS = {
    "question": {"top_left": (1749, 723), "bottom_right": (3017, 836)},
    "A": {"top_left": (1658, 995), "bottom_right": (2344, 1104)},
    "B": {"top_left": (2437, 997), "bottom_right": (3123, 1108)},
    "C": {"top_left": (1657, 1129), "bottom_right": (2345, 1241)},
    "D": {"top_left": (2437, 1131), "bottom_right": (3124, 1239)},
}

def click_button(button: int) -> None:
    """Click the specified button based on its coordinates."""
    screen_width, screen_height = pyautogui.size()
    x, y = BUTTON_COORDS[button]
    pyautogui.click(int(screen_width * x), int(screen_height * y))

def ollama_answer(question_and_answers: str) -> int:
    """Send the question to Ollama and return the answer."""
    try:
        response = ollama.generate(
            model="llama3.2",
            prompt=f"System: You are a highly focused assistant designed exclusively to answer multiple-choice questions. Your task is to analyze the question and the provided answer options, then respond only with the button number (1, 2, 3, or 4) that corresponds to the most likely correct answer. Do not include any additional text, explanations, or commentary in your response. If you are unsure of the answer, make an educated guess and still respond with only the button number. Your response must always be a single integer between 1 and 4.\n\nQuestion: {question_and_answers}"
        )
        reply = response.get("response", "").strip()
        if not reply:
            raise ValueError("Empty response from Ollama")
        return int(reply)
    except Exception as e:
        print(f"Error with Ollama: {e}")
        return None

def reconstruct_question(question: str, options: Dict[str, str]) -> str:
    """Reconstruct the question with options."""
    question = question.replace("____", "{blank}") if "____" in question else question
    return f"{question}\n" + "\n".join(f"{k}: {v}" for k, v in options.items())

def capture_text(region: Dict[str, Tuple[int, int]]) -> str:
    """Capture and extract text from a specified region."""
    x1, y1 = region["top_left"]
    x2, y2 = region["bottom_right"]
    screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
    return pytesseract.image_to_string(screenshot).strip()

def kahoot_god() -> None:
    """Main function to extract question, get answer, and click the button."""
    question, options = "", {}
    for element, coords in REGIONS.items():
        text = capture_text(coords)
        if text:
            if element == "question":
                question = text
            else:
                options[element] = text

    if question and options:
        full_question = reconstruct_question(question, options)
        answer = ollama_answer(full_question)
        if answer:
            click_button(answer)
        else:
            print("No answer received from Ollama.")
    else:
        print("Failed to extract question or options.")

# Bind the function to a hotkey
keyboard.add_hotkey("ctrl+alt+t", kahoot_god)
print("Press Ctrl+Alt+T to trigger the function.")
keyboard.wait()