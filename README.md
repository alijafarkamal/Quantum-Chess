# ♟️ Quantum Chess

**Quantum-enhanced chess move prediction using quantum algorithms**

Built for **CQHack25** - A global quantum hackathon project that demonstrates quantum computing applications in game theory and decision making.

## 🎯 Features

### 🎮 **Dual Mode Interface**
- **Play Game**: Real chess game against quantum AI
- **Move Analysis**: Position analysis and move suggestion tool

### ♟️ **Play Mode (Real Game)**
- **Interactive Chess Game**: Play against quantum AI with clean, Lichess-inspired interface
- **Keyboard Input Interface**: Enter moves in standard chess notation (e.g., "e4", "Nf3")
- **User as White**: You play White, quantum AI plays Black
- **Turn-Based Gameplay**: Make moves, quantum AI responds
- **Game Controls**: New game, resign, move history displayed in right sidebar
- **Real-Time Analysis**: Quantum AI thinks and plays moves
- **Three-Column Layout**: Move input on left, chess board in center, history on right

### 🔬 **Move Analysis Mode**
- **Position Analysis**: Set up any chess position for analysis
- **FEN String Support**: Input custom positions using standard FEN notation
- **Quantum Algorithm Selection**: Choose between Quantum Walk and Quantum Grover
- **Move Prediction**: Get quantum-inspired move suggestions
- **Probability Distribution**: Shows quantum sampling results with move probabilities
- **Game Continuation**: Continue playing from any position after quantum moves
- **FEN String Management**: Copy FEN strings from both original and new positions
- **Move History**: Track and view the sequence of quantum moves
- **Real-time Visualization**: See before/after board states with highlighted moves

## 🧰 Technologies

- **Frontend**: Streamlit, python-chess, SVG rendering
- **Quantum**: Quantum Walk (graph exploration) + Quantum Grover (amplitude amplification)
- **Chess Logic**: python-chess library
- **Visualization**: matplotlib, chess.svg

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/CQHack25-chess
   cd CQHack25-chess
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:8501`

## 🎮 How to Use

### **Main Menu**
When you open the app, you'll see two main options:

1. **♟️ Play Game** - Start a real chess game
2. **🔬 Move Analysis** - Analyze specific positions

### **Play Mode (Real Game)**
1. **Start Game**: Click "Play Game"
2. **Make Moves**: Enter moves in standard chess notation (e.g., "e4", "Nf3", "Qh5")
3. **Submit Move**: Click "Make Move" button to submit your move
4. **Quantum Response**: Watch the quantum AI respond with its move
5. **Game Controls**: Use "New Game" to restart or "Resign" to quit
6. **Move History**: View the complete game history in the right sidebar

### **Move Analysis Mode**
1. **Set up a position**:
   - Use the default starting position, or
   - Enter a FEN string in the input field
   - Click "Validate FEN" to confirm

2. **Run Quantum Analysis**:
   - Choose your preferred algorithm (Quantum Walk or Quantum Grover)
   - Click "Run Quantum Move Predictor"
   - Watch the quantum algorithm analyze all legal moves
   - See the selected move highlighted on the board

3. **Continue Playing**:
   - Click "Continue from New Position" to start from the resulting position
   - View move history to track your quantum game
   - Reset to starting position anytime

## ⚛️ Quantum Computing Implementation

### How Quantum Computing is Used

The application implements quantum-inspired algorithms for chess move selection:

#### 1. **Quantum Walk Algorithm**
- **Graph Exploration**: Builds a directed graph of future positions up to 3 moves deep
- **Connectivity Analysis**: Scores moves based on position connectivity and future options
- **Quantum-Inspired Scoring**: Uses √(connectivity) to mimic quantum amplitude growth
- **Blunder Prevention**: Explores tactical consequences to avoid obvious mistakes

#### 2. **Quantum Grover Algorithm**
- **Amplitude Amplification**: Uses Grover's algorithm to enhance the probability of finding the best move
- **Quantum State Preparation**: Creates quantum state with amplitudes proportional to move scores
- **Quantum Measurement**: Samples the quantum state to select moves
- **Probability Distribution**: Shows quantum sampling results with move probabilities

#### 3. **Quantum State Preparation**
- **Qiskit Implementation**: Uses genuine quantum state preparation with Qiskit
- **Amplitude Encoding**: Encodes move scores as quantum amplitudes
- **Quantum Superposition**: Demonstrates quantum superposition in move selection
- **Measurement**: Collapses quantum state to select the optimal move

### Key Quantum Components

1. **`quantum/quantum_walk.py`**: Implements quantum walk for position exploration
2. **`quantum/grover_move_selector.py`**: Implements Grover's algorithm for move selection
3. **`quantum/amplitude_selector.py`**: Handles quantum amplitude sampling
4. **`chess_logic/quantum_walk_eval.py`**: Evaluates positions using quantum walk

### Quantum Advantage

- **Superposition**: Evaluates multiple moves simultaneously
- **Interference**: Quantum interference enhances good moves and suppresses bad ones
- **Amplitude Amplification**: Grover's algorithm provides quadratic speedup
- **Future Exploration**: Quantum walk explores future positions more efficiently

## 📁 Project Structure

```
CQHack25-chess/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                # This file
├── chess_logic/
│   ├── __init__.py          # Package initialization
│   ├── move_eval.py         # Move scoring and evaluation
│   ├── board_utils.py       # FEN parsing and board utilities
│   └── quantum_walk_eval.py # Quantum walk evaluation
├── quantum/
│   ├── __init__.py          # Package initialization
│   ├── amplitude_selector.py # Quantum amplitude sampling
│   ├── grover_move_selector.py # Grover algorithm implementation
│   └── quantum_walk.py      # Quantum walk algorithm
└── test_files/
    ├── demo.py              # Demo scripts
    ├── test_app.py          # Test files
    └── ...                  # Other test files
```

## 🎯 Example FEN Strings

Try these interesting positions:

**Scholar's Mate Setup:**
```
rnbqkbnr/pppp1ppp/8/4p3/5Q2/8/PPPP1PPP/RNB1KBNR b KQkq - 3 3
```

**Fool's Mate:**
```
rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
```

**Endgame Position:**
```
8/8/8/8/8/8/4K3/4k3 w - - 0 1
```

## 🔧 Customization

### Adding New Evaluation Functions

Edit `chess_logic/move_eval.py` to implement custom scoring:

```python
def custom_evaluate_move(board, move):
    # Your custom evaluation logic here
    return score
```

### Modifying Quantum Parameters

Adjust quantum algorithm parameters in `quantum/grover_move_selector.py`:

```python
# Change number of shots
shots = 2000  # Default: 1000

# Modify optimal iterations
optimal_iterations = 15  # Default: calculated dynamically
```

## 🐛 Troubleshooting

### Common Issues

1. **Qiskit Installation**: If you encounter Qiskit installation issues:
   ```bash
   pip install qiskit[all]
   ```

2. **Streamlit Port**: If port 8501 is busy:
   ```bash
   streamlit run app.py --server.port 8502
   ```

3. **Memory Issues**: For large positions, the quantum algorithm may use significant memory. The app includes automatic fallback to classical algorithms.

### Error Handling

The application includes robust error handling:
- Invalid FEN strings are caught and reported
- Quantum algorithm failures fall back to classical methods
- Network issues with Qiskit are handled gracefully

## 🤝 Contributing

This project was built for CQHack25. Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **CQHack25** organizers for the quantum hackathon opportunity
- **Qiskit** team for the quantum computing framework
- **python-chess** developers for the excellent chess library
- **Streamlit** team for the interactive web framework

---

**Built with ♟️ and ⚛️ for the future of quantum computing in gaming!** 