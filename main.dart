import 'package:flutter/material.dart';

void main() {
  runApp(const CryptoEngineApp());
}

class CryptoEngineApp extends StatelessWidget {
  const CryptoEngineApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Crypto Engine',
      theme: ThemeData.dark(),
      home: const HomeScreen(),
    );
  }
}

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final List<Map<String, String>> cryptoList = [
    {"name": "Bitcoin", "symbol": "BTC", "price": "\$94,916.11", "change": "+2.5%"},
    {"name": "Ethereum", "symbol": "ETH", "price": "\$3,559.40", "change": "-1.8%"},
    {"name": "Litecoin", "symbol": "LTC", "price": "\$94.82", "change": "-0.5%"},
    {"name": "Solana", "symbol": "SOL", "price": "\$236.4", "change": "+1.2%"},
    {"name": "Cardano", "symbol": "ADA", "price": "\$1.00", "change": "−0.012%"},
  ];
  final List<Map<String, String>> chatHistory = [];
  final TextEditingController _chatController = TextEditingController();
  String chatbotMessage = "How can CryptoBot help you?";

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Crypto Engine'),
actions: [
  // Search Icon
  IconButton(
    icon: const Icon(Icons.search),
    onPressed: () {
      // Placeholder for search functionality
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Search coming soon!')),
      );
    },
  ),
  // Settings Icon
IconButton(
  icon: const Icon(Icons.settings),
  onPressed: () {
    // Navigate to Settings Page
    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => const SettingsPage()),
    );
  },
),
  // Profile Icon
  IconButton(
    icon: const CircleAvatar(
      backgroundColor: Colors.grey,
      child: Icon(Icons.person, color: Colors.white),
    ),
    onPressed: () {
      // Navigate to the Profile Page
      Navigator.push(
        context,
        MaterialPageRoute(builder: (context) => const ProfilePage()),
      );
    },
  ),
],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Real-Time Prices',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            // List of Cryptocurrencies
            Expanded(
              child: ListView.builder(
                itemCount: cryptoList.length,
                itemBuilder: (context, index) {
                  final crypto = cryptoList[index];
                  return Card(
                    child: ListTile(
                      leading: const Icon(Icons.currency_bitcoin, color: Colors.amber),
                      title: Text('${crypto["name"]} (${crypto["symbol"]})'),
                      subtitle: Text('Price: ${crypto["price"]}'),
                      trailing: Text(
                        '${crypto["change"]}',
                        style: TextStyle(
                          color: crypto["change"]!.startsWith('+') ? Colors.green : Colors.red,
                        ),
                      ),
                    ),
                  );
                },
              ),
            ),
            const SizedBox(height: 20),
            // Navigation Buttons for Reports and Predictions
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                ElevatedButton(
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (context) => const ReportsScreen()),
                    );
                  },
                  child: const Text('Reports'),
                ),
                ElevatedButton(
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (context) => const PredictionsScreen()),
                    );
                  },
                  child: const Text('Predictions'),
                ),
              ],
            ),
            const SizedBox(height: 20),
           Expanded(
  child: Column(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      const Text(
        'Chatbot',
        style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
      ),
      const SizedBox(height: 10),
      // Chat messages displayed here
      Expanded(
        child: ListView.builder(
          itemCount: chatHistory.length,
          itemBuilder: (context, index) {
            final message = chatHistory[index];
            final isUser = message['sender'] == 'user';
            return Align(
              alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
              child: Container(
                margin: const EdgeInsets.symmetric(vertical: 5.0),
                padding: const EdgeInsets.all(12.0),
                decoration: BoxDecoration(
                  color: isUser ? Colors.blue : Colors.grey.shade800,
                  borderRadius: BorderRadius.only(
                    topLeft: const Radius.circular(12.0),
                    topRight: const Radius.circular(12.0),
                    bottomLeft: isUser
                        ? const Radius.circular(12.0)
                        : const Radius.circular(0),
                    bottomRight: isUser
                        ? const Radius.circular(0)
                        : const Radius.circular(12.0),
                  ),
                ),
                child: Text(
                  message['message']!,
                  style: const TextStyle(color: Colors.white),
                ),
              ),
            );
          },
        ),
      ),
      const SizedBox(height: 10),
      // Chat input field
      Row(
        children: [
          Expanded(
            child: TextField(
              controller: _chatController,
              decoration: const InputDecoration(
                hintText: "Enter your query...",
                border: OutlineInputBorder(),
              ),
            ),
          ),
          const SizedBox(width: 10),
          ElevatedButton(
            onPressed: () {
              if (_chatController.text.isNotEmpty) {
                setState(() {
                  // Add user message to chat history
                  chatHistory.add({
                    'sender': 'user',
                    'message': _chatController.text,
                  });

                  // Add bot response
                  chatHistory.add({
                    'sender': 'bot',
                    'message':
                        "I'm learning! You asked: ${_chatController.text}",
                  });

                  _chatController.clear();
                });
              }
            },
            child: const Icon(Icons.send),
          ),
        ],
      ),
    ],
  ),
),

            const SizedBox(height: 20),
            // Display chatbot message
            Container(
              padding: const EdgeInsets.all(16.0),
              decoration: BoxDecoration(
                color: Colors.blueGrey.shade800,
                borderRadius: BorderRadius.circular(8),
              ),
              child: Text(
                chatbotMessage,
                style: const TextStyle(color: Colors.white),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class ReportsScreen extends StatelessWidget {
  const ReportsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Crypto Reports'),
      ),
      body: const Center(
        child: Text(
          'Here are the Crypto Reports.',
          style: TextStyle(fontSize: 24),
        ),
      ),
    );
  }
}

class PredictionsScreen extends StatelessWidget {
  const PredictionsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Crypto Predictions'),
      ),
      body: const Center(
        child: Text(
          'Here are the Crypto Predictions.',
          style: TextStyle(fontSize: 24),
        ),
      ),
    );
  }
}

class ProfilePage extends StatelessWidget {
  const ProfilePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('My Profile'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            // Profile Picture
            const CircleAvatar(
              radius: 50,
              backgroundColor: Colors.grey,
              child: Icon(Icons.person, size: 50, color: Colors.white), // Placeholder icon
            ),
            const SizedBox(height: 20),

            const Text(
              'Name: Moiz',
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            const Text(
              'Email: moiz@giki.com',
              style: TextStyle(fontSize: 16, color: Colors.grey),
            ),
            const SizedBox(height: 20),

            // Additional Information
            const Card(
              elevation: 2,
              margin: EdgeInsets.symmetric(vertical: 10),
              child: ListTile(
                leading: Icon(Icons.pie_chart, color: Colors.amber),
                title: Text('Total Portfolio Value'),
                trailing: Text('\$15,230.7', style: TextStyle(fontWeight: FontWeight.bold)),
              ),
            ),
            const Card(
              elevation: 2,
              margin: EdgeInsets.symmetric(vertical: 10),
              child: ListTile(
                leading: Icon(Icons.swap_vert, color: Colors.blue),
                title: Text('Total Trades'),
                trailing: Text('12', style: TextStyle(fontWeight: FontWeight.bold)),
              ),
            ),
            const Card(
              elevation: 2,
              margin: EdgeInsets.symmetric(vertical: 10),
              child: ListTile(
                leading: Icon(Icons.show_chart, color: Colors.green),
                title: Text('Successful Predictions'),
                trailing: Text('781', style: TextStyle(fontWeight: FontWeight.bold)),
              ),
            ),
            const Spacer(),

            ElevatedButton.icon(
              onPressed: () {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Account Settings coming soon!')),
                );
              },
              icon: const Icon(Icons.settings),
              label: const Text('Account Settings'),
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                textStyle: const TextStyle(fontSize: 16),
              ),
            ),
          ],
        ),
      ),
    );
  }
}


class SettingsPage extends StatelessWidget {
  const SettingsPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () {
            Navigator.pop(context); // Go back to the previous screen
          },
        ),
        title: const Text('Settings'),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16.0),
        children: [
          // Account Settings Section
          const Text(
            'Settings',
            style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 20),
          ListTile(
  leading: const Icon(Icons.person),
  title: const Text('Account Settings'),
  subtitle: const Text('Manage profile details and email'),
  onTap: () {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => const AccountSettingsPage()),
    );
  },
),

          ListTile(
            leading: const Icon(Icons.account_balance_wallet),
            title: const Text('Manage Wallets'),
            subtitle: const Text('Add, remove, or view wallet balances'),
            onTap: () {
              // Manage Wallets Placeholder
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Wallet Management coming soon!')),
              );
            },
          ),
          ListTile(
            leading: const Icon(Icons.lock),
            title: const Text('Security Settings'),
            subtitle: const Text('Manage 2FA, passwords, and devices'),
            onTap: () {
              // Security Settings Placeholder
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Security Settings coming soon!')),
              );
            },
          ),
          ListTile(
            leading: const Icon(Icons.key),
            title: const Text('API Keys'),
            subtitle: const Text('Manage third-party application access'),
            onTap: () {
              // API Keys Placeholder
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('API Key Management coming soon!')),
              );
            },
          ),
          const Divider(),
          // Trading Preferences Section
          const Text(
            'Trading Preferences',
            style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 10),
          ListTile(
            leading: const Icon(Icons.notifications),
            title: const Text('Notification Settings'),
            subtitle: const Text('Customize notifications and alerts'),
            onTap: () {
              // Notification Settings Placeholder
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Notification Settings coming soon!')),
              );
            },
          ),
          ListTile(
            leading: const Icon(Icons.swap_horiz),
            title: const Text('Preferred Trading Pairs'),
            subtitle: const Text('Set up your favorite trading pairs'),
            onTap: () {
              // Preferred Trading Pairs Placeholder
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Trading Pairs coming soon!')),
              );
            },
          ),
          ListTile(
            leading: const Icon(Icons.bar_chart),
            title: const Text('Trading Strategies'),
            subtitle: const Text('Customize automated trading strategies'),
            onTap: () {
              // Trading Strategies Placeholder
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Trading Strategies coming soon!')),
              );
            },
          ),
          const Divider(),
          // Market Analysis Section
          const Text(
            'Market Analysis',
            style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 10),
          ListTile(
            leading: const Icon(Icons.trending_up),
            title: const Text('Market Indicators'),
            subtitle: const Text('Access technical indicators and charts'),
            onTap: () {
              // Market Indicators Placeholder
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Market Indicators coming soon!')),
              );
            },
          ),
          ListTile(
            leading: const Icon(Icons.price_change),
            title: const Text('Price Alerts'),
            subtitle: const Text('Set alerts for specific cryptocurrencies'),
            onTap: () {
              // Price Alerts Placeholder
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Price Alerts coming soon!')),
              );
            },
          ),
          const Divider(),
          // About Section
          const Text(
            'About',
            style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 10),
          ListTile(
            leading: const Icon(Icons.help),
            title: const Text('Help & Support'),
            subtitle: const Text('Access FAQs, guides, and contact support'),
            onTap: () {
              // Help & Support Placeholder
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Help & Support coming soon!')),
              );
            },
          ),
        ],
      ),
    );
  }
}



class AccountSettingsPage extends StatelessWidget {
  const AccountSettingsPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Account Settings'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () {
            Navigator.pop(context);
          },
        ),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16.0),
        children: [
          // Profile Section
          const Text(
            'Profile',
            style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 16),
          const Row(
            children: [
              CircleAvatar(
                radius: 40,
                backgroundColor: Colors.grey,
                child: Icon(Icons.person, size: 40, color: Colors.white),
              ),
              SizedBox(width: 16),
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Abdul Moiz',
                    style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                  ),
                  SizedBox(height: 4),
                  Text(
                    'moiz@giki.com',
                    style: TextStyle(fontSize: 16, color: Colors.grey),
                  ),
                ],
              ),
            ],
          ),
          const Divider(height: 40, thickness: 1),

          // Account Settings Section
          const Text(
            'Account Settings',
            style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 16),
          ListTile(
            leading: const Icon(Icons.person),
            title: const Text('Personal Information'),
            subtitle: const Text('Update your name, email, and other details'),
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const PersonalInformationPage()),
              );
            },
          ),

          ListTile(
            leading: const Icon(Icons.notifications),
            title: const Text('Notification Settings'),
            subtitle: const Text('Manage email, push, and SMS notifications'),
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                    builder: (context) => const NotificationSettingsPage()),
              );
            },
          ),

          ListTile(
            leading: const Icon(Icons.privacy_tip_outlined),
            title: const Text('Privacy and Security'),
            subtitle: const Text('Manage your privacy and security settings'),
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                    builder: (context) => const PrivacyAndSecurityPage()),
              );
            },
          ),

          ListTile(
            leading: const Icon(Icons.language),
            title: const Text('Language Preferences'),
            subtitle: const Text('Select your preferred language'),
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                    builder: (context) => const LanguagePreferencesPage()),
              );
            },
          ),

          ListTile(
            leading: const Icon(Icons.delete_forever),
            title: const Text('Delete Account'),
            subtitle: const Text('Permanently delete your account'),
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                    builder: (context) => const DeleteAccountPage()),
              );
            },
          ),



          
        ],
      ),
    );
  }
}



class PersonalInformationPage extends StatefulWidget {
  const PersonalInformationPage({Key? key}) : super(key: key);

  @override
  State<PersonalInformationPage> createState() =>
      _PersonalInformationPageState();
}

class _PersonalInformationPageState extends State<PersonalInformationPage> {
  final TextEditingController _nameController =
      TextEditingController(text: 'Abdul Moiz');
  final TextEditingController _emailController =
      TextEditingController(text: 'moiz@giki.com');
  final TextEditingController _phoneController =
      TextEditingController(text: '+923001234567');

  @override
  void dispose() {
    _nameController.dispose();
    _emailController.dispose();
    _phoneController.dispose();
    super.dispose();
  }

  void _saveChanges() {
    // Example of saving changes
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Your information has been updated!')),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Personal Information'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () {
            Navigator.pop(context);
          },
        ),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Edit Your Information',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            // Name Field
            TextField(
              controller: _nameController,
              decoration: const InputDecoration(
                labelText: 'Name',
                border: OutlineInputBorder(),
                prefixIcon: Icon(Icons.person),
              ),
            ),
            const SizedBox(height: 16),
            // Email Field
            TextField(
              controller: _emailController,
              decoration: const InputDecoration(
                labelText: 'Email',
                border: OutlineInputBorder(),
                prefixIcon: Icon(Icons.email),
              ),
            ),
            const SizedBox(height: 16),
            // Phone Field
            TextField(
              controller: _phoneController,
              decoration: const InputDecoration(
                labelText: 'Phone Number',
                border: OutlineInputBorder(),
                prefixIcon: Icon(Icons.phone),
              ),
              keyboardType: TextInputType.phone,
            ),
            const Spacer(),
            // Save Button
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: _saveChanges,
                child: const Text(
                  'Save Changes',
                  style: TextStyle(fontSize: 18),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}




class NotificationSettingsPage extends StatefulWidget {
  const NotificationSettingsPage({Key? key}) : super(key: key);

  @override
  State<NotificationSettingsPage> createState() =>
      _NotificationSettingsPageState();
}

class _NotificationSettingsPageState extends State<NotificationSettingsPage> {
  bool _emailNotifications = true;
  bool _pushNotifications = true;
  bool _smsAlerts = false;

  void _saveSettings() {
    // Example of saving changes
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Notification settings updated!')),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Notification Settings'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () {
            Navigator.pop(context);
          },
        ),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Manage Your Notifications',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            // Email Notifications Toggle
            SwitchListTile(
              title: const Text('Email Notifications'),
              subtitle: const Text('Receive updates via email'),
              value: _emailNotifications,
              onChanged: (value) {
                setState(() {
                  _emailNotifications = value;
                });
              },
            ),
            // Push Notifications Toggle
            SwitchListTile(
              title: const Text('Push Notifications'),
              subtitle: const Text('Receive updates as push notifications'),
              value: _pushNotifications,
              onChanged: (value) {
                setState(() {
                  _pushNotifications = value;
                });
              },
            ),
            // SMS Alerts Toggle
            SwitchListTile(
              title: const Text('SMS Alerts'),
              subtitle: const Text('Receive updates via SMS'),
              value: _smsAlerts,
              onChanged: (value) {
                setState(() {
                  _smsAlerts = value;
                });
              },
            ),
            const Spacer(),
            // Save Button
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: _saveSettings,
                child: const Text(
                  'Save Changes',
                  style: TextStyle(fontSize: 18),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}



class PrivacyAndSecurityPage extends StatefulWidget {
  const PrivacyAndSecurityPage({Key? key}) : super(key: key);

  @override
  State<PrivacyAndSecurityPage> createState() => _PrivacyAndSecurityPageState();
}

class _PrivacyAndSecurityPageState extends State<PrivacyAndSecurityPage> {
  bool _twoFactorAuth = false;
  bool _appPermissions = true;

  void _changePassword() {
    // Example logic for changing password
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Password change process initiated!')),
    );
  }

  void _saveSettings() {
    // Example logic for saving changes
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Privacy and security settings updated!')),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Privacy and Security'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () {
            Navigator.pop(context);
          },
        ),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Privacy and Security Settings',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            // Change Password Option
            ListTile(
              leading: const Icon(Icons.lock_outline),
              title: const Text('Change Password'),
              subtitle: const Text('Update your account password'),
              onTap: _changePassword,
            ),
            const Divider(),
            // Two-Factor Authentication Toggle
            SwitchListTile(
              title: const Text('Two-Factor Authentication'),
              subtitle: const Text('Enhance account security with 2FA'),
              value: _twoFactorAuth,
              onChanged: (value) {
                setState(() {
                  _twoFactorAuth = value;
                });
              },
            ),
            const Divider(),
            // App Permissions Toggle
            SwitchListTile(
              title: const Text('App Permissions'),
              subtitle: const Text('Manage app access to your account'),
              value: _appPermissions,
              onChanged: (value) {
                setState(() {
                  _appPermissions = value;
                });
              },
            ),
            const Spacer(),
            // Save Changes Button
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: _saveSettings,
                child: const Text(
                  'Save Changes',
                  style: TextStyle(fontSize: 18),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}



class LanguagePreferencesPage extends StatefulWidget {
  const LanguagePreferencesPage({Key? key}) : super(key: key);

  @override
  State<LanguagePreferencesPage> createState() =>
      _LanguagePreferencesPageState();
}

class _LanguagePreferencesPageState extends State<LanguagePreferencesPage> {
  String _selectedLanguage = 'English'; // Default language

  final List<String> _languages = [
    'English',
    'Spanish',
    'French',
    'German',
    'Chinese',
    'Japanese',
    'Arabic',
    'Hindi',
    'Portuguese',
    'Russian',
  ];

  void _saveLanguagePreference() {
    // Example logic for saving language preference
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Language preference set to $_selectedLanguage')),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Language Preferences'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () {
            Navigator.pop(context);
          },
        ),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Choose Your Language',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            // Language Selection List
            Expanded(
              child: ListView.builder(
                itemCount: _languages.length,
                itemBuilder: (context, index) {
                  return RadioListTile(
                    title: Text(_languages[index]),
                    value: _languages[index],
                    groupValue: _selectedLanguage,
                    onChanged: (value) {
                      setState(() {
                        _selectedLanguage = value!;
                      });
                    },
                  );
                },
              ),
            ),
            const Spacer(),
            // Save Changes Button
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: _saveLanguagePreference,
                child: const Text(
                  'Save Changes',
                  style: TextStyle(fontSize: 18),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}


class DeleteAccountPage extends StatelessWidget {
  const DeleteAccountPage({Key? key}) : super(key: key);

  void _deleteAccount(BuildContext context) {
    // Example logic for deleting the account
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('Account deleted successfully'),
        backgroundColor: Colors.red,
      ),
    );

    // Navigate the user to the login or home page after deletion
    Navigator.popUntil(context, (route) => route.isFirst);
  }

  void _showDeleteConfirmationDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Confirm Delete'),
        content: const Text(
          'Are you sure you want to delete your account? This action cannot be undone.',
        ),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.pop(context); // Close the dialog
            },
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.red,
            ),
            onPressed: () {
              Navigator.pop(context); // Close the dialog
              _deleteAccount(context); // Perform account deletion
            },
            child: const Text('Delete'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Delete Account'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () {
            Navigator.pop(context);
          },
        ),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Delete Your Account',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            const Text(
              'Deleting your account will permanently remove all your data. This action cannot be undone. If you’re sure, tap the button below.',
              style: TextStyle(fontSize: 16),
            ),
            const Spacer(),
            // Delete Account Button
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.red,
                ),
                onPressed: () {
                  _showDeleteConfirmationDialog(context);
                },
                child: const Text(
                  'Delete Account',
                  style: TextStyle(fontSize: 18),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
