# ♟️ Grover's Gambit

**Quantum-enhanced chess move prediction using Grover's Algorithm**

Built for **CQHack25** - A global quantum hackathon project that demonstrates quantum computing applications in game theory and decision making.

## 🎯 Features

### 🎮 **Dual Mode Interface**
- **Play with Quantum Computer**: Real chess game against quantum AI
- **Quantum Move Predictor**: Position analysis and move suggestion tool

### ♟️ **Play Mode (Real Game)**
- **Interactive Chess Game**: Play against quantum AI with clean, Lichess-inspired interface
- **Keyboard Input Interface**: Enter moves in standard chess notation (e.g., "e4", "Nf3")
- **User as White**: You play White, quantum AI plays Black
- **Turn-Based Gameplay**: Make moves, quantum AI responds
- **Game Controls**: New game, resign, move history displayed in right sidebar
- **Real-Time Analysis**: Quantum AI thinks and plays moves
- **Three-Column Layout**: Move input on left, chess board in center, history on right

### 🔬 **Predictor Mode (Analysis)**
- **Position Analysis**: Set up any chess position for analysis
- **FEN String Support**: Input custom positions using standard FEN notation
- **True Quantum State Preparation**: Uses Qiskit for genuine quantum amplitude encoding
- **Quantum Walk Algorithm**: Graph-based exploration of future positions (depth 2-3)
- **Amplitude Sampling**: Quantum state preparation with √(score) amplitudes
- **Probability Distribution**: Shows quantum sampling results with move probabilities
- **Blunder Prevention**: Explores tactical consequences to avoid obvious mistakes
- **Game Continuation**: Continue playing from any position after quantum moves
- **FEN String Management**: Copy FEN strings from both original and new positions
- **Move History**: Track and view the sequence of quantum moves
- **Real-time Visualization**: See before/after board states with highlighted moves
- **Classical Fallback**: Robust error handling with classical algorithm backup

## 🧰 Technologies

- **Frontend**: Streamlit, python-chess, SVG rendering
- **Quantum**: Quantum Walk (graph exploration) + Quantum Grover (amplitude amplification)
- **Chess Logic**: python-chess library
- **Graph Analysis**: NetworkX for position connectivity analysis
- **Visualization**: matplotlib, chess.svg

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/alijafarkamal/Grovers-Gambit
   cd Grovers-Gambit
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

1. **♟️ Play with Quantum Computer** - Start a real chess game
2. **🔬 Quantum Move Predictor** - Analyze specific positions

### **Play Mode (Real Game)**
1. **Start Game**: Click "Play with Quantum Computer"
2. **Make Moves**: Enter moves in standard chess notation (e.g., "e4", "Nf3", "Qh5")
3. **Submit Move**: Click "Make Move" button to submit your move
4. **Quantum Response**: Watch the quantum AI respond with its move
5. **Game Controls**: Use "New Game" to restart or "Resign" to quit
6. **Move History**: View the complete game history in the right sidebar
7. **Clean Interface**: Enjoy the Lichess-inspired minimalist design

### **Predictor Mode (Analysis)**
1. **Set up a position**:
   - Use the default starting position, or
   - Enter a FEN string in the input field
   - Click "Validate FEN" to confirm

2. **Run Quantum Analysis**:
   - Choose your preferred algorithm (Quantum Walk or Quantum Grover)
   - Click "🚀 Run Quantum Move Predictor"
   - Watch the quantum algorithm analyze all legal moves
   - See the selected move highlighted on the board

3. **Continue Playing**:
   - Click "🎯 Continue from New Position" to start from the resulting position
   - Use "📋 Copy FEN Strings" to get both position FENs
   - View move history to track your quantum game
   - Reset to starting position anytime

4. **View Results**:
   - Compare original vs. new position
   - See the move notation (e.g., "e4", "Nf3")
   - Check game status (check, checkmate, etc.)

## 🔬 Quantum Algorithm Details

### True Quantum Algorithm Implementation

The app implements genuine quantum computing techniques:

#### 🔬 Quantum Walk with Graph Exploration
1. **Graph Construction**: Builds a directed graph of future positions up to 3 moves deep
2. **Connectivity Analysis**: Scores moves based on position connectivity and future options
3. **Quantum-Inspired Scoring**: Uses √(connectivity) to mimic quantum amplitude growth
4. **Blunder Prevention**: Explores tactical consequences to avoid obvious mistakes
5. **Selection**: Returns the move with the highest future potential

#### ⚛️ Quantum Amplitude Sampling
1. **State Preparation**: Creates quantum state with amplitudes ∝ √(move_score)
2. **Qiskit Implementation**: Uses genuine quantum state preparation with Qiskit
3. **Quantum Measurement**: Samples the quantum state to select moves
4. **Probability Distribution**: Shows quantum sampling results with move probabilities
5. **Quantum Advantage**: Demonstrates quantum superposition in move selection

#### 🎯 Classical Baseline
1. **Material Evaluation**: Simple material counting for comparison
2. **Baseline Performance**: Shows improvement over classical methods
3. **Validation**: Ensures quantum methods perform better than random selection

### Scoring System

- **Material Values**: Pawn=1, Knight=3, Bishop=3, Rook=5, Queen=9, King=0
- **Tactical Bonuses**: 
  - Checkmate: +1000
  - Check: +50
  - Capture: +10

## 📁 Project Structure

```
quantum-move-predictor/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                # This file
├── chess_logic/
│   ├── __init__.py          # Package initialization
│   ├── move_eval.py         # Move scoring and evaluation
│   ├── board_utils.py       # FEN parsing and board utilities
│   └── quantum_walk_eval.py # Quantum walk evaluation
└── quantum/
    ├── __init__.py          # Package initialization
    ├── amplitude_selector.py # Quantum amplitude sampling
    ├── grover_move_selector.py # Grover algorithm implementation
    └── quantum_walk.py      # Quantum walk algorithm
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