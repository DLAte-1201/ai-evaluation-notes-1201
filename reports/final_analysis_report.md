# AI Response Evaluation Final Analysis Report

## 1. Project Overview
이 프로젝트는 AI 응답을 사람이 직접 평가하기 위한 휴먼 인 더 루프(Human-in-the-loop) 평가 프로젝트이다.

## 2. Dataset Summary
총 10개의 프롬프트를 사용했다.
프롬프트 유형은 사실 확인, 출처 추적, 제한 조건 준수, 요약, 비교 분석, 절차 안내, 안전 민감 질문, 한국어 사투리, 모호한 맥락, 미래 예측으로 구성했다.

## 3. Evaluation Method
각 응답은 8개 기준으로 0~4점 평가했다.
평가 기준은 지시 준수성, 사실 정확성, 완성도, 논리 품질, 명확성, 안전성, 한국어 맥락 적합성, 간결성이다.

## 4. Key Findings
주요 결함은 다음과 같았다.

1. 출처 귀속 오류
2. 근거 없는 정밀 확률 제시
3. 요약 요청에 대한 과도한 장문 응답
4. 모호한 질문을 특정 의도로 과잉 해석
5. 공식 출처 대신 2차 출처에 의존

## 5. Strong Responses
안전 민감 질문과 한국어 사투리 해석 응답은 비교적 품질이 높았다.

## 6. Weak Responses
금융 예측형 응답은 구조는 좋았지만, 확률과 가격 범위가 지나치게 정밀하게 제시되어 과신을 유도할 수 있었다.

## 7. What I Learned
AI 응답 평가는 단순히 답이 그럴듯한지 보는 작업이 아니라, 사용자의 의도, 출처 품질, 지시 준수, 안전성, 표현의 불확실성을 함께 평가하는 QA 작업에 가깝다는 점을 확인했다.

## 8. Portfolio Relevance
이 프로젝트는 AI Evaluator, QA Tester, SQA Engineer, AI Data Quality Analyst 직무와 연결된다.