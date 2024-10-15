import React from 'react';
import { StyleSheet, Text, View, TouchableOpacity, TextInput } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';

export default function TabTwoScreen() {
  const router = useRouter();

  const handleBTCPress = () => {
    router.push('/BTCscreen');
  };

  const handleETHPress = () => {
    router.push('/ETHscreen');
  };

  const handleSOLPress = () => {
    router.push('/SOLscreen');
  };

  const handleSettingsPress = () => {
    router.push('/settings'); // Linking to settings.tsx
  };

  const handleProfilePress = () => {
    router.push('/userprofile'); // Linking to userprofile.tsx
  };

  return (
    <View style={styles.container}>
      {/* Settings button (top left) */}
      <TouchableOpacity style={styles.settingsButton} onPress={handleSettingsPress}>
        <Ionicons name="settings-outline" size={30} color={styles.iconColor.color} />
      </TouchableOpacity>

      {/* User profile button (top right) */}
      <TouchableOpacity style={styles.profileButton} onPress={handleProfilePress}>
        <Ionicons name="person-circle-outline" size={30} color={styles.iconColor.color} />
      </TouchableOpacity>

      {/* Coin buttons */}
      <View style={styles.buttonContainer}>
        <TouchableOpacity style={styles.ovalButton} onPress={handleBTCPress}>
          <View style={styles.buttonContent}>
            <Text style={styles.buttonText}>BTC</Text>
            <View style={styles.dummyValueContainer}>
              <Text style={styles.dummyValueTextGreen}>$40,000</Text>
              <Ionicons name="arrow-up" size={16} color="green" />
            </View>
          </View>
        </TouchableOpacity>
        <TouchableOpacity style={styles.ovalButton} onPress={handleETHPress}>
          <View style={styles.buttonContent}>
            <Text style={styles.buttonText}>ETH</Text>
            <View style={styles.dummyValueContainer}>
              <Text style={styles.dummyValueTextRed}>$2,500</Text>
              <Ionicons name="arrow-down" size={16} color="red" />
            </View>
          </View>
        </TouchableOpacity>
        <TouchableOpacity style={styles.ovalButton} onPress={handleSOLPress}>
          <View style={styles.buttonContent}>
            <Text style={styles.buttonText}>SOL</Text>
            <View style={styles.dummyValueContainer}>
              <Text style={styles.dummyValueTextGreen}>$150</Text>
              <Ionicons name="arrow-up" size={16} color="green" />
            </View>
          </View>
        </TouchableOpacity>
      </View>

      {/* Merged Text Input and Send Button */}
      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          placeholder="How can CryptoBot help you?"
          placeholderTextColor="#03161a"
        />
        <TouchableOpacity style={styles.sendButton}>
          <Ionicons name="send" size={24} color="#FFFFFF" />
        </TouchableOpacity>
      </View>
    </View>
  );
}

// Styles remain the same

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'space-between',
    paddingTop: 50,
    paddingHorizontal: 20,
    backgroundColor: '#F9F9F9',
  },
  buttonContainer: {
    alignItems: 'center',
    justifyContent: 'flex-start',
    flex: 1,
    paddingTop: 40,
  },
  ovalButton: {
    backgroundColor: '#4A90E2',
    paddingVertical: 15,
    paddingHorizontal: 20,
    borderRadius: 50,
    marginVertical: 5,
    alignItems: 'flex-start',
    width: '90%',
    borderColor: '#D6D9FF',
    borderWidth: 2,
  },
  buttonContent: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    width: '100%',
  },
  buttonText: {
    fontSize: 24,
    color: '#FFFFFF',
    fontWeight: 'bold',
    textAlign: 'left',
    flex: 1, // Allow button text to take available space
  },
  dummyValueContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  dummyValueTextGreen: {
    fontSize: 18,
    color: 'green',
    textAlign: 'right',
    marginRight: 5, // Space between value and arrow
  },
  dummyValueTextRed: {
    fontSize: 18,
    color: 'red',
    textAlign: 'right',
    marginRight: 5, // Space between value and arrow
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 20,
  },
  input: {
    height: 50,
    borderRadius: 50,
    backgroundColor: '#FFFFFF',
    borderColor: '#00dab7',
    borderWidth: 2,
    paddingHorizontal: 20,
    fontSize: 18,
    color: '#333333',
    flex: 1, // Allow input to take available space
    marginRight: 10, // Space between input and send button
  },
  sendButton: {
    backgroundColor: '#4A90E2',
    borderRadius: 50,
    padding: 10,
    justifyContent: 'center',
    alignItems: 'center',
  },
  settingsButton: {
    position: 'absolute',
    top: 20,
    left: 20,
  },
  profileButton: {
    position: 'absolute',
    top: 20,
    right: 20,
  },
  iconColor: {
    color: '#4A90E2',
  },
});
