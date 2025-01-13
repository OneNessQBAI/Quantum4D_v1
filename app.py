import streamlit as st
import cirq
import numpy as np
import matplotlib.pyplot as plt

st.title("4D Quantum State Simulation")
st.write("""
This application demonstrates how quantum computing can represent higher-dimensional
states through multi-qubit systems and quantum operations.
""")

# Create a 2-qubit system (representing a 4D state space)
q0, q1 = cirq.LineQubit.range(2)

def create_4d_circuit(theta1, theta2):
    """Create a quantum circuit that explores 4D concepts through 2-qubit operations"""
    circuit = cirq.Circuit()
    
    # Initialize superposition to access all dimensions
    circuit.append([
        cirq.H(q0),  # Hadamard on first qubit
        cirq.H(q1)   # Hadamard on second qubit
    ])
    
    # Create entanglement (representing higher-dimensional correlations)
    circuit.append(cirq.CNOT(q0, q1))
    
    # Apply rotations in different "dimensions"
    circuit.append([
        cirq.rx(theta1).on(q0),  # Rotation in X-Z plane
        cirq.ry(theta2).on(q1)   # Rotation in Y-Z plane
    ])
    
    # Add measurements
    circuit.append([
        cirq.measure(q0, key='q0'),
        cirq.measure(q1, key='q1')
    ])
    
    return circuit

# Sidebar controls
st.sidebar.header("Circuit Parameters")
theta1 = st.sidebar.slider("θ1 (X-Z rotation)", 0.0, 2*np.pi, np.pi/2)
theta2 = st.sidebar.slider("θ2 (Y-Z rotation)", 0.0, 2*np.pi, np.pi/2)

try:
    # Create circuit for state vector simulation (without measurements)
    circuit_no_measure = create_4d_circuit(theta1, theta2)[:-1]  # Exclude measurements
    circuit_with_measure = create_4d_circuit(theta1, theta2)     # Include measurements
    
    simulator = cirq.Simulator()
    result = simulator.simulate(circuit_no_measure)

    # Display circuit
    st.subheader("Quantum Circuit")
    st.text(str(circuit_with_measure))

    # Visualize state vector
    st.subheader("State Vector Visualization")

    # Convert state vector to density matrix for better visualization
    state_vector = result.final_state_vector
    density_matrix = np.outer(state_vector, np.conjugate(state_vector))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    # Plot amplitude
    probabilities = np.abs(state_vector)**2
    ax1.bar(range(4), probabilities)
    ax1.set_title("State Probabilities")
    ax1.set_xlabel("Basis State")
    ax1.set_ylabel("Probability")
    ax1.set_xticks(range(4))
    ax1.set_xticklabels(['|00⟩', '|01⟩', '|10⟩', '|11⟩'])

    # Plot density matrix
    im = ax2.imshow(np.real(density_matrix), cmap='RdBu')
    ax2.set_title("Density Matrix (Real Part)")
    plt.colorbar(im, ax=ax2)
    ax2.set_xticks(range(4))
    ax2.set_yticks(range(4))
    ax2.set_xticklabels(['|00⟩', '|01⟩', '|10⟩', '|11⟩'])
    ax2.set_yticklabels(['|00⟩', '|01⟩', '|10⟩', '|11⟩'])

    st.pyplot(fig)

    # Explanation
    st.subheader("Understanding 4D Representation")
    st.write("""
    The simulation above demonstrates how quantum computing can represent higher-dimensional
    states using multiple qubits:

    1. **Two-Qubit System**: Using 2 qubits gives us access to a 4-dimensional Hilbert space,
       with basis states |00⟩, |01⟩, |10⟩, and |11⟩.

    2. **Superposition**: The Hadamard gates create superpositions, allowing the state to exist
       in multiple dimensions simultaneously.

    3. **Entanglement**: The CNOT gate creates quantum correlations that can't be separated
       into individual qubit states, representing higher-dimensional relationships.

    4. **Rotations**: The rx and ry gates perform rotations in different planes of the
       4D space, showing how we can manipulate higher-dimensional quantum states.
    """)

    # Display measurement statistics
    st.subheader("Measurement Statistics")
    measurements = simulator.run(circuit_with_measure, repetitions=1000)
    
    # Process measurements
    results = []
    for q0, q1 in zip(measurements.measurements['q0'], measurements.measurements['q1']):
        results.append(f"{q0[0]}{q1[0]}")
    
    # Count occurrences
    from collections import Counter
    counts = Counter(results)
    measurement_dict = {f"|{k}⟩": v/1000 for k, v in counts.items()}
    
    st.bar_chart(measurement_dict)

    # Add Bloch sphere representation
    st.subheader("Individual Qubit States")
    st.write("""
    While the system as a whole exists in 4D, we can visualize the individual qubit states
    by calculating their reduced density matrices. This gives us a projection of each qubit's
    state, though it doesn't capture the full quantum correlations.
    """)

    # Calculate reduced density matrices
    rho_0 = np.trace(density_matrix.reshape(2, 2, 2, 2), axis1=1, axis2=3)
    rho_1 = np.trace(density_matrix.reshape(2, 2, 2, 2), axis1=0, axis2=2)

    # Display the reduced density matrices
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    
    im1 = ax1.imshow(np.real(rho_0), cmap='RdBu')
    ax1.set_title("Qubit 0 State")
    plt.colorbar(im1, ax=ax1)
    
    im2 = ax2.imshow(np.real(rho_1), cmap='RdBu')
    ax2.set_title("Qubit 1 State")
    plt.colorbar(im2, ax=ax2)
    
    st.pyplot(fig)

except Exception as e:
    st.error(f"An error occurred during simulation: {str(e)}")
    st.write("Please try adjusting the parameters or refreshing the page.")