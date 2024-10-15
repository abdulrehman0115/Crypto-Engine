import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView } from 'react-native';

const BtcScreen = () => {
    return (
        <ScrollView style={styles.container}>
            {/* Title */}
            <Text style={styles.title}>Bitcoin Stock Graph</Text>

            {/* Placeholder for the Graph */}
            <View style={styles.graphContainer}>
                <View style={styles.dummyGraph} />
            </View>

            {/* Indication Button */}
            <TouchableOpacity style={styles.button}>
                <Text style={styles.buttonText}>Indication</Text>
            </TouchableOpacity>

            {/* Generate Report Button */}
            <TouchableOpacity style={styles.button}>
                <Text style={styles.buttonText}>Generate Report</Text>
            </TouchableOpacity>
        </ScrollView>
    );
};

// Styles
const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#f0f0f0',
        paddingHorizontal: 20,
        paddingVertical: 10,
    },
    title: {
        fontSize: 24,
        fontWeight: 'bold',
        textAlign: 'center',
        marginBottom: 20,
        color: '#333',
    },
    graphContainer: {
        alignItems: 'center',
        marginBottom: 30,
    },
    dummyGraph: {
        width: '100%', // Use full width of the container
        height: 200, // Fixed height for the outline
        borderWidth: 2,
        borderColor: '#007BFF', // Outline color
        borderRadius: 10,
        backgroundColor: 'rgba(0, 123, 255, 0.1)', // Light background color for visibility
    },
    button: {
        backgroundColor: '#007BFF',
        padding: 15,
        borderRadius: 10,
        marginBottom: 20,
        alignItems: 'center',
    },
    buttonText: {
        color: '#fff',
        fontSize: 16,
        fontWeight: 'bold',
    },
});

export default BtcScreen;
