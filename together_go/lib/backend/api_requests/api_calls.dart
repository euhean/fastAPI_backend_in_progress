import 'dart:convert';
import 'dart:typed_data';

import '/flutter_flow/flutter_flow_util.dart';
import 'api_manager.dart';

export 'api_manager.dart' show ApiCallResponse;

const _kPrivateApiFunctionName = 'ffPrivateApiCall';

class UserCall {
  static Future<ApiCallResponse> call({
    String? email = '',
    String? name = '',
    String? birthdate = '',
    String? password = '',
  }) async {
    final ffApiRequestBody = '''
{
  "name": "",
  "email": "",
  "birthdate": "",
  "gender": "",
  "telephone": "",
  "adress": "",
  "city": "",
  "postal_code": "",
  "country": "",
  "job": "",
  "company": "",
  "hobbies": "",
  "language": "",
  "topics": "",
  "notifications": "",
  "consent": "",
  "password": ""
}''';
    return ApiManager.instance.makeApiCall(
      callName: 'User',
      apiUrl:
          'http://192.168.43.175:8000/docs#/default/create_user_users__post',
      callType: ApiCallType.POST,
      headers: {},
      params: {},
      body: ffApiRequestBody,
      bodyType: BodyType.JSON,
      returnBody: true,
      encodeBodyUtf8: false,
      decodeUtf8: false,
      cache: false,
      alwaysAllowBody: false,
    );
  }
}

class ApiPagingParams {
  int nextPageNumber = 0;
  int numItems = 0;
  dynamic lastResponse;

  ApiPagingParams({
    required this.nextPageNumber,
    required this.numItems,
    required this.lastResponse,
  });

  @override
  String toString() =>
      'PagingParams(nextPageNumber: $nextPageNumber, numItems: $numItems, lastResponse: $lastResponse,)';
}

String _serializeList(List? list) {
  list ??= <String>[];
  try {
    return json.encode(list);
  } catch (_) {
    return '[]';
  }
}

String _serializeJson(dynamic jsonVar, [bool isList = false]) {
  jsonVar ??= (isList ? [] : {});
  try {
    return json.encode(jsonVar);
  } catch (_) {
    return isList ? '[]' : '{}';
  }
}
