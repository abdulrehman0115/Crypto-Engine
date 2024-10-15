import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView, Image } from 'react-native';

const UserProfile = () => {
    return (
        <ScrollView style={styles.container}>
            {/* User Info */}
            <View style={styles.header}>
                <Image
                    source={{ uri: 'https://placekitten.com/200/200' }} // Placeholder for profile picture
                    style={styles.profilePic}
                />
                <Text style={styles.userName}>Umair</Text>
                <Text style={styles.userEmail}>umairslav@giki.com</Text>
            </View>

            {/* Account Overview */}
            <View style={styles.accountOverview}>
                <Text style={styles.sectionTitle}>Account Overview</Text>
                <View style={styles.accountInfo}>
                    <Text style={styles.label}>Total Portfolio Value:</Text>
                    <Text style={styles.value}>$15,230.75</Text>
                </View>
                <View style={styles.accountInfo}>
                    <Text style={styles.label}>Total Trades:</Text>
                    <Text style={styles.value}>128</Text>
                </View>
                <View style={styles.accountInfo}>
                    <Text style={styles.label}>Successful Predictions:</Text>
                    <Text style={styles.value}>78%</Text>
                </View>
            </View>

            {/* Trade History */}
            <View style={styles.tradeHistory}>
                <Text style={styles.sectionTitle}>Recent Trades</Text>
                {/* Replace these with dynamic data later */}
                <View style={styles.tradeItem}>
                    <Text style={styles.tradeLabel}>BTC</Text>
                    <Text style={styles.tradeValue}>+2.5%</Text>
                </View>
                <View style={styles.tradeItem}>
                    <Text style={styles.tradeLabel}>ETH</Text>
                    <Text style={styles.tradeValue}>-1.3%</Text>
                </View>
                <View style={styles.tradeItem}>
                    <Text style={styles.tradeLabel}>SOL</Text>
                    <Text style={styles.tradeValue}>+0.8%</Text>
                </View>
            </View>

            {/* Settings Button */}
            <TouchableOpacity style={styles.button}>
                <Text style={styles.buttonText}>Account Settings</Text>
            </TouchableOpacity>
        </ScrollView>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#f0f0f0',
        paddingHorizontal: 20,
    },
    header: {
        alignItems: 'center',
        marginVertical: 20,
    },
    profilePic: {
        width: 100,
        height: 100,
        borderRadius: 50,
        marginBottom: 10,
    },
    userName: {
        fontSize: 24,
        fontWeight: 'bold',
    },
    userEmail: {
        fontSize: 16,
        color: '#555',
    },
    accountOverview: {
        marginVertical: 20,
    },
    sectionTitle: {
        fontSize: 18,
        fontWeight: 'bold',
        marginBottom: 10,
    },
    accountInfo: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        marginBottom: 10,
    },
    label: {
        fontSize: 16,
        color: '#333',
    },
    value: {
        fontSize: 16,
        fontWeight: 'bold',
    },
    tradeHistory: {
        marginVertical: 20,
    },
    tradeItem: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        marginBottom: 10,
        padding: 10,
        backgroundColor: '#fff',
        borderRadius: 5,
    },
    tradeLabel: {
        fontSize: 16,
    },
    tradeValue: {
        fontSize: 16,
        fontWeight: 'bold',
    },
    button: {
        backgroundColor: '#007BFF',
        padding: 15,
        borderRadius: 5,
        alignItems: 'center',
        marginVertical: 20,
    },
    buttonText: {
        color: '#fff',
        fontSize: 16,
        fontWeight: 'bold',
    },
});

export default UserProfile;
