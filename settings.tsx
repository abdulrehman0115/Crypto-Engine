import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView } from 'react-native';

const Settings = () => {
    return (
        <View style={styles.container}>
            <View style={styles.header}>
                <TouchableOpacity style={{ marginTop: 5 }}>
                    <Text style={styles.backButton}>⬅️</Text>
                </TouchableOpacity>
                <Text style={styles.headerTitle}>Settings</Text>
                <View style={{ width: 30 }} />
            </View>
            <ScrollView style={styles.content}>
                <Text style={styles.sectionTitle}>Account Settings</Text>
                <TouchableOpacity style={styles.button}>
                    <Text style={styles.buttonText}>Manage Wallets</Text>
                </TouchableOpacity>
                <TouchableOpacity style={styles.button}>
                    <Text style={styles.buttonText}>Security Settings</Text>
                </TouchableOpacity>
                <TouchableOpacity style={styles.button}>
                    <Text style={styles.buttonText}>API Keys</Text>
                </TouchableOpacity>

                <Text style={styles.sectionTitle}>Trading Preferences</Text>
                <TouchableOpacity style={styles.button}>
                    <Text style={styles.buttonText}>Notification Settings</Text>
                </TouchableOpacity>
                <TouchableOpacity style={styles.button}>
                    <Text style={styles.buttonText}>Preferred Trading Pairs</Text>
                </TouchableOpacity>
                <TouchableOpacity style={styles.button}>
                    <Text style={styles.buttonText}>Trading Strategies</Text>
                </TouchableOpacity>

                <Text style={styles.sectionTitle}>Market Analysis</Text>
                <TouchableOpacity style={styles.button}>
                    <Text style={styles.buttonText}>Market Indicators</Text>
                </TouchableOpacity>
                <TouchableOpacity style={styles.button}>
                    <Text style={styles.buttonText}>Price Alerts</Text>
                </TouchableOpacity>

                <Text style={styles.sectionTitle}>About</Text>
                <TouchableOpacity style={styles.button}>
                    <Text style={styles.buttonText}>Help & Support</Text>
                </TouchableOpacity>
                <TouchableOpacity style={styles.button}>
                    <Text style={styles.buttonText}>Terms of Service</Text>
                </TouchableOpacity>
                <TouchableOpacity style={styles.button}>
                    <Text style={styles.buttonText}>Privacy Policy</Text>
                </TouchableOpacity>
            </ScrollView>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#f8f8f8',
    },
    header: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        paddingHorizontal: 20,
        paddingVertical: 10,
        backgroundColor: '#fff',
        borderBottomWidth: 1,
        borderBottomColor: '#ddd',
    },
    backButton: {
        fontSize: 20,
    },
    headerTitle: {
        fontSize: 20,
        fontWeight: 'bold',
    },
    content: {
        padding: 20,
    },
    sectionTitle: {
        fontSize: 16,
        fontWeight: 'bold',
        marginBottom: 10,
    },
    button: {
        backgroundColor: '#ddd',
        paddingVertical: 15,
        paddingHorizontal: 10,
        marginBottom: 10,
        borderRadius: 5,
    },
    buttonText: {
        fontSize: 16,
    },
});

export default Settings;
