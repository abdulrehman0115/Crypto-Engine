import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:fl_chart/fl_chart.dart'; // Required for FlSpot

class BinanceService {
  // Fetch the current price and 24h change of a cryptocurrency
  static Future<Map<String, dynamic>> fetchPrice(String symbol) async {
    final String url = 'https://api.binance.com/api/v3/ticker/24hr?symbol=${symbol}USDT';

    try {
      final response = await http.get(Uri.parse(url));

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        double? price = double.tryParse(data["lastPrice"] ?? "0.0");
        double? change = double.tryParse(data["priceChangePercent"] ?? "0.0");

        return {"price": price ?? 0.0, "change": change ?? 0.0};
      }
    } catch (e) {
      print("Error fetching Binance data: $e");
    }
    return {"price": 0.0, "change": 0.0};
  }

  // Fetch detailed BTC-specific market data
  static Future<Map<String, dynamic>> fetchBTCDetails() async {
    final String url = 'https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT';

    try {
      final response = await http.get(Uri.parse(url));

      if (response.statusCode == 200) {
        final data = json.decode(response.body);

        return {
          "price": double.tryParse(data["lastPrice"] ?? "0.0") ?? 0.0,
          "change": double.tryParse(data["priceChangePercent"] ?? "0.0") ?? 0.0,
          "marketCap": double.tryParse(data["quoteVolume"] ?? "0.0") ?? 0.0, // Approximate Market Cap
          "volume": double.tryParse(data["volume"] ?? "0.0") ?? 0.0,
        };
      }
    } catch (e) {
      print("Error fetching BTC details: $e");
    }
    return {"price": 0.0, "change": 0.0, "marketCap": 0.0, "volume": 0.0};
  }

  // Fetch historical prices for any cryptocurrency
  static Future<List<FlSpot>> fetchPriceHistory(String symbol) async {
    final String url =
        'https://api.binance.com/api/v3/klines?symbol=${symbol}USDT&interval=1h&limit=7';

    try {
      final response = await http.get(Uri.parse(url));

      if (response.statusCode == 200) {
        final data = json.decode(response.body) as List;

        // Convert the response to FlSpot for charting
        return data.asMap().entries.map<FlSpot>((entry) {
          final index = entry.key.toDouble(); // Time (e.g., 0, 1, 2...)
          final closingPrice = double.parse(entry.value[4]); // Closing price
          return FlSpot(index, closingPrice);
        }).toList();
      } else {
        print('Failed to fetch historical data for $symbol: ${response.statusCode}');
      }
    } catch (e) {
      print("Error fetching historical data for $symbol: $e");
    }
    return [];
  }

  // Fetch detailed market data for any coin (e.g., market cap, volume)
  static Future<Map<String, dynamic>> fetchDetailedMarketData(String symbol) async {
    final String url = 'https://api.binance.com/api/v3/ticker/24hr?symbol=${symbol}USDT';

    try {
      final response = await http.get(Uri.parse(url));

      if (response.statusCode == 200) {
        final data = json.decode(response.body);

        return {
          "price": double.tryParse(data["lastPrice"] ?? "0.0") ?? 0.0,
          "change": double.tryParse(data["priceChangePercent"] ?? "0.0") ?? 0.0,
          "marketCap": double.tryParse(data["quoteVolume"] ?? "0.0") ?? 0.0,
          "volume": double.tryParse(data["volume"] ?? "0.0") ?? 0.0,
        };
      }
    } catch (e) {
      print("Error fetching detailed market data for $symbol: $e");
    }
    return {"price": 0.0, "change": 0.0, "marketCap": 0.0, "volume": 0.0};
  }
}
