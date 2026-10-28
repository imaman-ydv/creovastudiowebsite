import 'dart:convert';

import 'package:http/http.dart' as http;

const apiBaseUrl = String.fromEnvironment(
  'API_BASE_URL',
  defaultValue: 'http://127.0.0.1:8000/api',
);

class SiteApi {
  SiteApi({http.Client? client}) : _client = client ?? http.Client();

  final http.Client _client;

  Future<List<ProjectSummary>> fetchProjects() async {
    final response = await _client.get(Uri.parse('$apiBaseUrl/projects/'));
    _throwForStatus(response);
    final data = jsonDecode(response.body) as Map<String, dynamic>;
    return (data['results'] as List<dynamic>)
        .map((item) => ProjectSummary.fromJson(item as Map<String, dynamic>))
        .toList();
  }

  Future<List<InsightSummary>> fetchInsights() async {
    final response = await _client.get(Uri.parse('$apiBaseUrl/insights/'));
    _throwForStatus(response);
    final data = jsonDecode(response.body) as Map<String, dynamic>;
    return (data['results'] as List<dynamic>)
        .map((item) => InsightSummary.fromJson(item as Map<String, dynamic>))
        .toList();
  }

  Future<void> submitContact({
    required String name,
    required String email,
    required String message,
  }) async {
    final response = await _client.post(
      Uri.parse('$apiBaseUrl/contact/'),
      headers: const {'Content-Type': 'application/json'},
      body: jsonEncode({'name': name, 'email': email, 'message': message}),
    );
    _throwForStatus(response);
  }

  void _throwForStatus(http.Response response) {
    if (response.statusCode < 200 || response.statusCode >= 300) {
      var message = 'The request could not be completed.';
      try {
        final body = jsonDecode(response.body) as Map<String, dynamic>;
        message = body['error']?.toString() ?? message;
      } on FormatException {
        // Keep the friendly fallback for non-JSON server errors.
      }
      throw SiteApiException(message);
    }
  }
}

class SiteApiException implements Exception {
  const SiteApiException(this.message);

  final String message;

  @override
  String toString() => message;
}

class ProjectSummary {
  const ProjectSummary({
    required this.title,
    required this.slug,
    required this.client,
    required this.year,
    required this.category,
    required this.summary,
    required this.coverImageUrl,
    required this.websiteUrl,
    required this.featured,
  });

  final String title;
  final String slug;
  final String client;
  final int? year;
  final String category;
  final String summary;
  final String coverImageUrl;
  final String websiteUrl;
  final bool featured;

  factory ProjectSummary.fromJson(Map<String, dynamic> json) => ProjectSummary(
        title: json['title']?.toString() ?? '',
        slug: json['slug']?.toString() ?? '',
        client: json['client']?.toString() ?? '',
        year: json['year'] as int?,
        category: json['category']?.toString() ?? '',
        summary: json['summary']?.toString() ?? '',
        coverImageUrl: json['cover_image_url']?.toString() ?? '',
        websiteUrl: json['website_url']?.toString() ?? '',
        featured: json['featured'] == true,
      );
}

class InsightSummary {
  const InsightSummary({
    required this.title,
    required this.slug,
    required this.excerpt,
    required this.coverImageUrl,
    required this.body,
    required this.publishedAt,
  });

  final String title;
  final String slug;
  final String excerpt;
  final String coverImageUrl;
  final String body;
  final String? publishedAt;

  factory InsightSummary.fromJson(Map<String, dynamic> json) => InsightSummary(
        title: json['title']?.toString() ?? '',
        slug: json['slug']?.toString() ?? '',
        excerpt: json['excerpt']?.toString() ?? '',
        coverImageUrl: json['cover_image_url']?.toString() ?? '',
        body: json['body']?.toString() ?? '',
        publishedAt: json['published_at']?.toString(),
      );
}
