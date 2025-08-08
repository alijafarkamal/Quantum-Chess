# ♟️ Quantum Chess

**Quantum-enhanced chess move prediction using genuine quantum circuits**

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
- **Four Quantum Algorithms**: Choose between QAOA, True Quantum Walk, Quantum Walk, and Quantum Grover
- **Move Prediction**: Get quantum-inspired move suggestions
- **Probability Distribution**: Shows quantum sampling results with move probabilities
- **Game Continuation**: Continue playing from any position after quantum moves
- **FEN String Management**: Copy FEN strings from both original and new positions
- **Move History**: Track and view the sequence of quantum moves
- **Real-time Visualization**: See before/after board states with highlighted moves

## 🧰 Technologies

- **Frontend**: Streamlit, python-chess, SVG rendering
- **Quantum**: QAOA (optimization) + True Quantum Walk (Qiskit circuits) + Quantum Grover (amplitude amplification)
- **Chess Logic**: python-chess library
- **Data Science**: NumPy, Pandas, NetworkX, Matplotlib
- **Visualization**: matplotlib, chess.svg
- **Version Control**: Git, GitHub

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/Quantum-Chess
   cd Quantum-Chess
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
   - Choose your preferred algorithm:
     - **QAOA (Optimization)**: Frames move selection as optimization problem
     - **True Quantum Walk (Qiskit)**: Genuine quantum circuit implementation
     - **Quantum Walk (Intelligent)**: Graph-based exploration
     - **Quantum Grover (Classic)**: Amplitude amplification
   - Click "Run Quantum Move Predictor"
   - Watch the quantum algorithm analyze all legal moves
   - See the selected move highlighted on the board

3. **Continue Playing**:
   - Click "Continue from New Position" to start from the resulting position
   - View move history to track your quantum game
   - Reset to starting position anytime

## ⚛️ Quantum Computing Implementation

### How Quantum Computing is Used

The application implements **genuine quantum computing** using Qiskit circuits:

#### 1. **QAOA (Quantum Approximate Optimization Algorithm)**
- **Optimization Approach**: Frames move selection as optimization problem
- **Cost Function**: Minimizes negative evaluation scores
- **Phase Separator**: RZ gates with move scores as phases
- **Mixing Hamiltonian**: RX gates for exploration
- **Parameter Optimization**: Multiple gamma/beta combinations
- **Quantum Advantage**: Explores solution space in superposition

#### 2. **True Quantum Walk (Qiskit Circuits)**
- **Coined Quantum Walk**: Uses auxiliary qubit for direction control
- **Coin Operator**: Hadamard gate for unbiased coin flip
- **Shift Operator**: Controlled operations for state transitions
- **Quantum State Preparation**: Creates quantum state with amplitudes proportional to move scores
- **Quantum Measurement**: Collapses superposition to select optimal moves
- **Interference Effects**: Quantum interference enhances good moves and suppresses bad ones

#### 3. **Quantum Walk Algorithm (Graph Exploration)**
- **Graph Construction**: Builds a directed graph of future positions up to 3 moves deep
- **Connectivity Analysis**: Scores moves based on position connectivity and future options
- **Quantum-Inspired Scoring**: Uses √(connectivity) to mimic quantum amplitude growth
- **Blunder Prevention**: Explores tactical consequences to avoid obvious mistakes

#### 4. **Quantum Grover Algorithm**
- **Amplitude Amplification**: Uses Grover's algorithm to enhance the probability of finding the best move
- **Quantum State Preparation**: Creates quantum state with amplitudes proportional to move scores
- **Quantum Measurement**: Samples the quantum state to select moves
- **Probability Distribution**: Shows quantum sampling results with move probabilities

### Key Quantum Components

1. **`quantum/qaoa_move_selector.py`**: Implements QAOA for optimization-based move selection
2. **`quantum/quantum_walk.py`**: Implements true quantum walk with Qiskit circuits
3. **`quantum/grover_move_selector.py`**: Implements Grover's algorithm for move selection
4. **`quantum/amplitude_selector.py`**: Handles quantum amplitude sampling
5. **`chess_logic/quantum_walk_eval.py`**: Evaluates positions using quantum walk
6. **`chess_logic/board_utils.py`**: Generates move graphs for quantum exploration

### Enhanced Evaluation System

The application includes a comprehensive board evaluation function that considers:
- **Material Advantage**: Proper piece values (Pawn=100, Knight=320, Bishop=330, Rook=500, Queen=900)
- **Mobility**: Number of legal moves available
- **King Safety**: Check detection and penalties
- **Center Control**: Positional bonuses for center squares
- **Pawn Structure**: Advanced pawn bonuses
- **Piece Activity**: Center piece bonuses
- **Development**: Early game considerations

### Quantum Advantage

- **Superposition**: Evaluates multiple moves simultaneously
- **Interference**: Quantum interference enhances good moves and suppresses bad ones
- **Amplitude Amplification**: Grover's algorithm provides quadratic speedup
- **Future Exploration**: Quantum walk explores future positions more efficiently
- **Genuine Quantum Circuits**: Uses real Qiskit quantum circuits instead of heuristics
- **Optimization Focus**: QAOA finds optimal moves rather than just searching

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
│   ├── qaoa_move_selector.py # QAOA optimization implementation
│   └── quantum_walk.py      # True quantum walk with Qiskit circuits
└── test_files/
    ├── demo.py              # Demo scripts
    ├── test_app.py          # Test files
    ├── test_true_quantum_walk.py # True quantum walk tests
    ├── test_qaoa_move_selector.py # QAOA tests
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

Adjust quantum algorithm parameters:

```python
# QAOA parameters
gamma_values = [0.5, 1.0, 1.5]  # Phase separator strength
beta_values = [0.5, 1.0, 1.5]   # Mixing strength

# Quantum Walk parameters
shots = 2048  # Number of quantum measurements
steps = 3     # Walk depth
```

### Testing Quantum Algorithms

Run the dedicated test suites:

```bash
# Test True Quantum Walk
python3 test_files/test_true_quantum_walk.py

# Test QAOA
python3 test_files/test_qaoa_move_selector.py
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
- True quantum walk has multiple fallback mechanisms
- QAOA includes parameter optimization and classical fallbacks

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

**Built with:** Python, Streamlit, Qiskit, python-chess, NetworkX, NumPy, Pandas, Matplotlib, SVG, HTML/CSS, Git, GitHub

**Built with ♟️ and ⚛️ for the future of quantum computing in gaming!** 
