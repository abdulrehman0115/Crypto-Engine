import 'package:flutter/material.dart';
import 'services/binance_service.dart';
import 'login_screen.dart';
import 'dart:async'; // Import for Timer
import 'package:fl_chart/fl_chart.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

void main() {
  runApp(const CryptoEngineApp());
}

class CryptoEngineApp extends StatelessWidget {
  const CryptoEngineApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Crypto Engine',
      theme: ThemeData.dark(),
      home: const LoginScreen(),
    );
  }
}

class HomeScreen extends StatefulWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  _HomeScreenState createState() => _HomeScreenState();
}


class _HomeScreenState extends State<HomeScreen> {
  final List<Map<String, String>> cryptoList = [
    {"name": "Bitcoin", "symbol": "BTC", "price": "Loading...", "change": "0.00%", "logo": "assets/logos/btc.png"},
    {"name": "Ethereum", "symbol": "ETH", "price": "Loading...", "change": "0.00%", "logo": "assets/logos/eth.png"},
    {"name": "Solana", "symbol": "SOL", "price": "Loading...", "change": "0.00%", "logo": "assets/logos/sol.jpeg"},
  ];

  bool isLoading = false;
  Timer? _timer; // Timer for auto-updating

  @override
  void initState() {
    super.initState();
    fetchPrices(); // Fetch immediately on launch
    _startAutoUpdate(); // Start automatic refresh every 30 seconds
  }

  @override
  void dispose() {
    _timer?.cancel(); // Stop timer when widget is disposed
    super.dispose();
  }

  // Function to fetch live prices from Binance API
  Future<void> fetchPrices() async {
    setState(() {
      isLoading = true;
    });

    try {
      for (int i = 0; i < cryptoList.length; i++) {
        String symbol = cryptoList[i]["symbol"] ?? "";

        // Fetch price and change from Binance
        Map<String, dynamic> data = await BinanceService.fetchPrice(symbol);
        double price = data["price"] ?? 0.0;
        double change = data["change"] ?? 0.0;

        setState(() {
          cryptoList[i]["price"] = '\$${price.toStringAsFixed(2)}';
          cryptoList[i]["change"] = '${change.toStringAsFixed(2)}%';
        });
      }
    } catch (e) {
      print("Error fetching prices: $e");
    }

    setState(() {
      isLoading = false;
    });
  }

  // Automatically refresh prices every 30 seconds
  void _startAutoUpdate() {
    _timer = Timer.periodic(const Duration(seconds: 30), (Timer t) {
      fetchPrices();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Crypto Engine'),
        actions: [
          IconButton(
            icon: const Icon(Icons.search),
            onPressed: () {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Search coming soon!')),
              );
            },
          ),
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: fetchPrices, // Manual refresh button
          ),
          IconButton(
            icon: const Icon(Icons.settings),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const AccountSettingsPage()),
              );
            },
          ),
          IconButton(
            icon: const CircleAvatar(
              backgroundColor: Colors.grey,
              child: Icon(Icons.person, color: Colors.white),
            ),
            onPressed: () {
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
              'Real-Time Prices ',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            isLoading
                ? const Center(child: CircularProgressIndicator())
                : Expanded(
                    child: ListView.builder(
  itemCount: cryptoList.length,
  itemBuilder: (context, index) {
    final crypto = cryptoList[index];
    // Correctly parse priceChange
    double priceChange = double.tryParse(
      crypto["change"]?.replaceAll('%', '').trim() ?? "0.0",
    ) ?? 0.0;

    return Card(
      child: ListTile(
        leading: crypto["logo"] != null && crypto["logo"]!.isNotEmpty
            ? Image.asset(
                crypto["logo"]!,
                width: 40,
                height: 40,
                errorBuilder: (context, error, stackTrace) =>
                    const Icon(Icons.currency_bitcoin, color: Colors.amber),
              )
            : const Icon(Icons.currency_bitcoin, color: Colors.amber),
        title: Text('${crypto["name"] ?? "Unknown"} (${crypto["symbol"] ?? "N/A"})'),
        subtitle: Text('Price: ${crypto["price"] ?? "Loading..."}'),
        trailing: Text(
          crypto["change"] ?? "0.00%",
          style: TextStyle(
            fontWeight: FontWeight.bold,
            color: priceChange >= 0 ? Colors.green : Colors.red,
          ),
        ),
        onTap: () {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => CoinDetailsScreen(
                name: crypto["name"]!,
                symbol: crypto["symbol"]!,
                logo: crypto["logo"]!,
              ),
            ),
          );
        },
      ),
    );
  },
),
                  ),
            const SizedBox(height: 20),
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
            Row(
              children: [
                Expanded(
                  child: TextField(
                    decoration: const InputDecoration(
                      hintText: "Enter your query...",
                      border: OutlineInputBorder(),
                    ),
                  ),
                ),
                const SizedBox(width: 10),
                ElevatedButton(
                  onPressed: () {
                    // Placeholder for sending a query
                  },
                  child: const Icon(Icons.send),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

class ReportsScreen extends StatelessWidget {
  const ReportsScreen({Key? key}) : super(key: key);

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
  const PredictionsScreen({Key? key}) : super(key: key);

  final List<Map<String, String>> cryptoList = const [
    {"name": "Bitcoin", "symbol": "BTC", "logo": "assets/logos/btc.png"},
    {"name": "Ethereum", "symbol": "ETH", "logo": "assets/logos/eth.png"},
    {"name": "Solana", "symbol": "SOL", "logo": "assets/logos/sol.jpeg"},
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Select a Coin for Prediction')),
      body: ListView.builder(
        itemCount: cryptoList.length,
        itemBuilder: (context, index) {
          final crypto = cryptoList[index];

          return Card(
            child: ListTile(
              leading: crypto["logo"] != null && crypto["logo"]!.isNotEmpty
                  ? Image.asset(
                      crypto["logo"]!,
                      width: 40,
                      height: 40,
                      errorBuilder: (context, error, stackTrace) =>
                          const Icon(Icons.currency_bitcoin, color: Colors.amber),
                    )
                  : const Icon(Icons.currency_bitcoin, color: Colors.amber),
              title: Text('${crypto["name"]} (${crypto["symbol"]})'),
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => SelectPredictionTimeScreen(
                      name: crypto["name"]!,
                      symbol: crypto["symbol"]!,
                      logo: crypto["logo"]!,
                    ),
                  ),
                );
              },
            ),
          );
        },
      ),
    );
  }
}

class SelectPredictionTimeScreen extends StatefulWidget {
  final String name;
  final String symbol;
  final String logo;

  const SelectPredictionTimeScreen({
    Key? key,
    required this.name,
    required this.symbol,
    required this.logo,
  }) : super(key: key);

  @override
  _SelectPredictionTimeScreenState createState() => _SelectPredictionTimeScreenState();
}

class _SelectPredictionTimeScreenState extends State<SelectPredictionTimeScreen> {
  String selectedTimePeriod = "";

  final List<Map<String, dynamic>> timePeriods = [
    {"label": "10 Minutes", "value": "10min"},
    {"label": "3 Hours", "value": "3hrs"},
    {"label": "24 Hours", "value": "24hrs"},
    {"label": "7 Days", "value": "7days"},
    {"label": "1 Month", "value": "1month"},
  ];

  void selectTimePeriod(String period) {
  setState(() {
    selectedTimePeriod = period;
  });

  // Show confirmation before proceeding
  showDialog(
    context: context,
    builder: (context) {
      return AlertDialog(
        title: const Text("Confirm Selection"),
        content: Text(
          "You selected:\n\n"
          "• Coin: ${widget.name} (${widget.symbol})\n"
          "• Time Period: $selectedTimePeriod\n\n"
          "Proceed to prediction?",
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context), // Cancel
            child: const Text("Cancel"),
          ),
          TextButton(
            onPressed: () {
              Navigator.pop(context); // Close dialog
              proceedToPrediction();
            },
            child: const Text("Confirm"),
          ),
        ],
      );
    },
  );
}

void proceedToPrediction() {
  Navigator.push(
    context,
    MaterialPageRoute(
      builder: (context) => PredictionResultsScreen(
        name: widget.name,
        symbol: widget.symbol,
        logo: widget.logo,
        timePeriod: selectedTimePeriod,
      ),
    ),
  );
}
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Select Time Period for ${widget.name} Prediction')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Image.asset(
              widget.logo,
              width: 80,
              height: 80,
              errorBuilder: (context, error, stackTrace) =>
                  const Icon(Icons.currency_bitcoin, size: 80, color: Colors.amber),
            ),
            const SizedBox(height: 20),
            const Text(
              "Choose a time period for prediction",
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 20),
            Expanded(
              child: ListView.builder(
                itemCount: timePeriods.length,
                itemBuilder: (context, index) {
                  final timePeriod = timePeriods[index];

                  return Card(
                    child: ListTile(
                      title: Text(timePeriod["label"]),
                      trailing: selectedTimePeriod == timePeriod["value"]
                          ? const Icon(Icons.check_circle, color: Colors.green)
                          : null,
                      onTap: () {
                        selectTimePeriod(timePeriod["value"]);
                      },
                    ),
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class PredictionResultsScreen extends StatefulWidget {
  final String name;
  final String symbol;
  final String logo;
  final String timePeriod;

  const PredictionResultsScreen({
    Key? key,
    required this.name,
    required this.symbol,
    required this.logo,
    required this.timePeriod,
  }) : super(key: key);

  @override
  _PredictionResultsScreenState createState() => _PredictionResultsScreenState();
}

class _PredictionResultsScreenState extends State<PredictionResultsScreen> {
  double currentPrice = 0.0;
  double predictedPrice = 0.0;
  bool isLoading = true;

  // ✅ Change this to the actual local IP of the PC running Flask
  final String apiUrl = "http://127.0.0.1:5001/predict"; // Replace with actual IP

  @override
  void initState() {
    super.initState();
    fetchPrediction();
  }

Future<void> fetchPrediction() async {
  setState(() {
    isLoading = true;
  });

  try {
    final Map<String, dynamic> requestBody = {
      "coin": widget.symbol,
      "time_period": widget.timePeriod,
    };

    print("📡 Sending request to API: $requestBody"); // Debugging

    // Call your Flask API to get the predicted price
    final response = await http.post(
      Uri.parse(apiUrl),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode(requestBody),
    );

    print("📡 Response received: ${response.statusCode}"); // Debugging

    if (response.statusCode == 200) {
      final data = jsonDecode(utf8.decode(response.bodyBytes));
      print("📡 API Data: $data"); // Debugging

      // Now fetch the current price from Binance
      final binanceData = await BinanceService.fetchPrice(widget.symbol);
      double currentPriceFetched = binanceData["price"] ?? 0.0;

      setState(() {
        predictedPrice = data["predicted_price"];
        currentPrice = currentPriceFetched;
        isLoading = false;
      });
    } else {
      throw Exception("Failed to fetch prediction");
    }
  } catch (e) {
    print("🚨 Error fetching prediction: $e");
    setState(() {
      isLoading = false;
    });
  }
}



  double calculatePercentageChange() {
    if (currentPrice == 0) return 0.0;
    return ((predictedPrice - currentPrice) / currentPrice) * 100;
  }

  @override
  Widget build(BuildContext context) {
    double percentageChange = calculatePercentageChange();
    return Scaffold(
      appBar: AppBar(title: Text('Prediction for ${widget.name}')),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: isLoading
              ? const Center(child: CircularProgressIndicator())
              : Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    Image.asset(
                      widget.logo,
                      width: 80,
                      height: 80,
                      errorBuilder: (context, error, stackTrace) =>
                          const Icon(Icons.currency_bitcoin, size: 80, color: Colors.amber),
                    ),
                    const SizedBox(height: 20),
                    Text(
                      "${widget.name} (${widget.symbol})",
                      style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: 20),
                    Text(
                      "Time Period: ${widget.timePeriod}",
                      style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w500),
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: 20),
                    Text(
                      "Current Price: \$${currentPrice.toStringAsFixed(2)}",
                      style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: 10),
                    Text(
                      "Predicted Price: \$${predictedPrice.toStringAsFixed(2)}",
                      style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.blue),
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: 10),
                    Text(
                      "Change: ${percentageChange.toStringAsFixed(2)}%",
                      style: TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                        color: percentageChange >= 0 ? Colors.green : Colors.red,
                      ),
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: 30),
                    ElevatedButton(
                      onPressed: () => Navigator.pop(context),
                      style: ElevatedButton.styleFrom(
                        padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                      ),
                      child: const Text("Go Back"),
                    ),
                  ],
                ),
        ),
      ),
    );
  }
}


class ProfilePage extends StatelessWidget {
  const ProfilePage({Key? key}) : super(key: key);

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
            Card(
              elevation: 2,
              margin: const EdgeInsets.symmetric(vertical: 10),
              child: ListTile(
                leading: const Icon(Icons.pie_chart, color: Colors.amber),
                title: const Text('Total Portfolio Value'),
                trailing: const Text('\$15,230.7', style: TextStyle(fontWeight: FontWeight.bold)),
              ),
            ),
            Card(
              elevation: 2,
              margin: const EdgeInsets.symmetric(vertical: 10),
              child: ListTile(
                leading: const Icon(Icons.swap_vert, color: Colors.blue),
                title: const Text('Total Trades'),
                trailing: const Text('12', style: TextStyle(fontWeight: FontWeight.bold)),
              ),
            ),
            Card(
              elevation: 2,
              margin: const EdgeInsets.symmetric(vertical: 10),
              child: ListTile(
                leading: const Icon(Icons.show_chart, color: Colors.green),
                title: const Text('Successful Predictions'),
                trailing: const Text('781', style: TextStyle(fontWeight: FontWeight.bold)),
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
  const SettingsPage({Key? key}) : super(key: key);

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
                MaterialPageRoute(builder: (context) => AccountSettingsPage()),
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
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => NotificationSettingsPage()),
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


class CoinDetailsScreen extends StatefulWidget {
  final String name;
  final String symbol;
  final String logo;

  const CoinDetailsScreen({
    Key? key,
    required this.name,
    required this.symbol,
    required this.logo,
  }) : super(key: key);

  @override
  _CoinDetailsScreenState createState() => _CoinDetailsScreenState();
}

class _CoinDetailsScreenState extends State<CoinDetailsScreen> {
  double price = 0.0;
  double priceChange = 0.0;
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    fetchData();
  }

  Future<void> fetchData() async {
    setState(() {
      isLoading = true;
    });

    // Fetch current price and 24h change
    final data = await BinanceService.fetchPrice(widget.symbol);
    setState(() {
      price = data["price"];
      priceChange = data["change"];
      isLoading = false;
    });
  }

  Widget _buildPriceChart() {
  return FutureBuilder<List<FlSpot>>(
    future: BinanceService.fetchPriceHistory(widget.symbol), // Fetch historical data
    builder: (context, snapshot) {
      if (snapshot.connectionState == ConnectionState.waiting) {
        return const Center(child: CircularProgressIndicator());
      }
      if (snapshot.hasError || !snapshot.hasData || snapshot.data!.isEmpty) {
        return const Center(
          child: Text(
            'Failed to load data',
            style: TextStyle(color: Colors.red),
          ),
        );
      }

      final spots = snapshot.data!;

      // Calculate min and max values dynamically
      double minY = spots.map((s) => s.y).reduce((a, b) => a < b ? a : b);
      double maxY = spots.map((s) => s.y).reduce((a, b) => a > b ? a : b);

      // Add padding to the Y-axis range to avoid overflow
      double padding = (maxY - minY) * 0.05; // 5% padding
      minY = minY - padding;
      maxY = maxY + padding;

      // Determine suitable interval for Y-axis labels
      double yInterval = (maxY - minY) / 6; // 6 labels max

      return LineChart(
        LineChartData(
          minY: minY,
          maxY: maxY,
          gridData: FlGridData(
            show: true,
            drawVerticalLine: true,
            horizontalInterval: yInterval,
            verticalInterval: 1,
            getDrawingHorizontalLine: (value) => FlLine(
              color: Colors.grey.withOpacity(0.5),
              strokeWidth: 1,
            ),
            getDrawingVerticalLine: (value) => FlLine(
              color: Colors.grey.withOpacity(0.5),
              strokeWidth: 1,
            ),
          ),
          titlesData: FlTitlesData(
            show: true,
            bottomTitles: AxisTitles(
              sideTitles: SideTitles(
                showTitles: true,
                interval: 1,
                getTitlesWidget: (value, meta) {
                  final intervals = ['0h', '4h', '8h', '12h', '16h', '20h', '24h'];
                  if (value.toInt() >= 0 && value.toInt() < intervals.length) {
                    return Padding(
                      padding: const EdgeInsets.only(top: 6),
                      child: Text(
                        intervals[value.toInt()],
                        style: const TextStyle(color: Colors.white, fontSize: 12),
                      ),
                    );
                  }
                  return const SizedBox();
                },
              ),
            ),
            leftTitles: AxisTitles(
              sideTitles: SideTitles(
                showTitles: true,
                interval: yInterval,
                reservedSize: 40, // Prevent overlap
                getTitlesWidget: (value, meta) {
                  return Padding(
                    padding: const EdgeInsets.only(right: 5),
                    child: Text(
                      '\$${(value / 1000).toStringAsFixed(1)}K', // Format values in 'K' notation
                      style: const TextStyle(color: Colors.white, fontSize: 12),
                    ),
                  );
                },
              ),
            ),
          ),
          borderData: FlBorderData(
            show: true,
            border: Border.all(color: Colors.grey, width: 1),
          ),
          lineBarsData: [
            LineChartBarData(
              spots: spots, // Use dynamic data
              isCurved: true,
              color: Colors.orange,
              barWidth: 4,
              isStrokeCapRound: true,
              belowBarData: BarAreaData(
                show: true,
                gradient: LinearGradient(
                  colors: [
                    Colors.orange.withOpacity(0.3),
                    Colors.deepOrange.withOpacity(0.1),
                  ],
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                ),
              ),
              dotData: FlDotData(
                show: true,
                checkToShowDot: (spot, barData) => true,
                getDotPainter: (spot, percent, barData, index) {
                  return FlDotCirclePainter(
                    radius: 3,
                    color: Colors.orange,
                    strokeWidth: 2,
                    strokeColor: Colors.white,
                  );
                },
              ),
            ),
          ],
        ),
      );
    },
  );
}

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('${widget.name} (${widget.symbol}) Details')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (isLoading)
              const Center(child: CircularProgressIndicator())
            else ...[
              Text(
                "Current Price: \$${price.toStringAsFixed(2)}",
                style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 10),
              Text(
                "24h Change: ${priceChange.toStringAsFixed(2)}%",
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: priceChange >= 0 ? Colors.green : Colors.red,
                ),
              ),
            ],
            const SizedBox(height: 20),
            const Text("Price Chart (24h)", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 10),
            Expanded(child: _buildPriceChart()),
          ],
        ),
      ),
    );
  }
}