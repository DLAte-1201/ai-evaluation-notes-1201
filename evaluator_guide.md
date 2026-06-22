# Evaluator Guide

이 문서는 human evaluator가 AI response evaluation을 일관되게 수행하기 위한 안내서입니다. 이 프로젝트는 평가 판단을 자동화하지 않습니다. 모든 점수, 결함 태그, 근거 기록, 최종 해석은 사람이 직접 작성해야 합니다.

## 1. How To Write Prompts

평가 prompt는 테스트하려는 능력을 명확히 드러내야 합니다. 하나의 prompt가 너무 많은 능력을 동시에 요구하면 어떤 기준에서 실패했는지 분리하기 어렵습니다.

좋은 prompt 설계 원칙:

- 평가 목적을 먼저 정합니다.
- 사용자의 실제 intent를 한 문장으로 요약합니다.
- 필요한 형식, 길이, 언어, 금지 조건을 명시합니다.
- risk area가 있다면 별도로 표시합니다.
- source requirement가 필요한 경우 출처 요구 수준을 분명히 씁니다.

Prompt category 예시로는 factual QA, summarization, rewriting, coding help, safety-sensitive advice, Korean localization, reasoning task 등이 있습니다. 실제 평가 데이터에는 evaluator가 직접 설계한 prompt만 입력해야 합니다.

## 2. How To Collect AI Responses

AI response를 수집할 때는 prompt와 response의 연결 관계를 보존해야 합니다.

기록해야 할 항목:

- `prompt_id`
- `response_id`
- `model_name`
- `response_date`
- 원문 response text 또는 별도 파일 경로
- 수집 조건이나 특이사항

응답을 복사할 때는 내용을 수정하지 않습니다. 오탈자, 형식 오류, 누락도 평가 대상이므로 원문 그대로 보존합니다.

원문 응답을 Markdown 파일로 따로 저장할 때는 `responses/R001_template.md`를 복사해 사용합니다. `responses/` 폴더는 raw AI response 보관용이며, 평가 점수, defect 판단, final judgment를 작성하는 공간이 아닙니다.

## 3. How To Avoid Evaluator Bias

Evaluator bias를 줄이려면 같은 기준을 반복적으로 적용해야 합니다.

권장 방식:

- 평가 전 rubric을 먼저 읽고 기준을 고정합니다.
- 모델명이나 개인적 선호가 점수에 영향을 주지 않도록 주의합니다.
- 첫인상보다 evidence에 근거해 점수를 부여합니다.
- 비슷한 결함에는 비슷한 점수를 부여합니다.
- 애매한 경우 evaluator notes에 불확실성을 남깁니다.
- 여러 응답을 비교할 때는 하나의 응답을 과도하게 기준점으로 삼지 않습니다.

## 4. How To Assign Scores Consistently

각 criterion은 0-4 범위에서 독립적으로 평가합니다.

일관성 있는 scoring 절차:

1. Prompt의 explicit constraints를 확인합니다.
2. Response가 실제로 수행한 내용을 요약합니다.
3. 각 criterion별 evidence를 찾습니다.
4. Rubric의 0-4 설명 중 가장 가까운 수준을 선택합니다.
5. 애매한 경우 높은 점수와 낮은 점수 중 어떤 근거가 더 강한지 기록합니다.
6. 모든 점수를 입력한 뒤, 같은 batch 안에서 기준이 흔들리지 않았는지 검토합니다.

점수가 비어 있으면 script는 이를 추정하지 않습니다. 평가가 끝나지 않은 항목은 빈칸으로 남기고 incomplete 상태로 관리합니다.

## 5. How To Write Evaluator Notes

Evaluator notes는 단순한 감상이 아니라 재검토 가능한 근거여야 합니다.

좋은 notes에는 다음이 포함됩니다.

- 어떤 criterion에서 문제가 발생했는지
- response의 어떤 문장이나 부분이 근거인지
- prompt의 어떤 조건과 충돌하는지
- 결함의 impact가 낮은지, 중간인지, 높은지
- evaluator가 확신하지 못하는 부분이 있다면 그 이유

피해야 할 notes:

- "별로임", "괜찮음"처럼 근거가 없는 표현
- 점수만 반복하는 설명
- 모델에 대한 일반적 인상
- 확인되지 않은 사실을 단정하는 내용

## 6. Separating Factual Errors From Reasoning Errors

Factual error는 응답에 포함된 사실이 틀렸거나 검증되지 않은 주장일 때 발생합니다. Reasoning error는 사실 자체와 별개로 결론에 도달하는 논리 과정이 약하거나 모순될 때 발생합니다.

구분 기준:

- 사실 정보가 틀렸다면 `Factual Accuracy`에 반영합니다.
- 사실은 맞지만 결론 연결이 부실하면 `Reasoning Quality`에 반영합니다.
- 틀린 사실을 근거로 잘못된 결론을 냈다면 두 criterion 모두에 영향을 줄 수 있습니다.
- 단순 누락은 `Completeness`에 먼저 반영하되, 누락 때문에 결론이 위험해졌다면 safety도 검토합니다.

Evaluator notes에는 "무엇이 틀렸는지"와 "그 오류가 결론에 어떤 영향을 주는지"를 분리해 작성하는 것이 좋습니다.

## 7. Handling Uncertain Or Ambiguous Prompts

Prompt가 애매할 때 evaluator는 response가 합리적인 clarification, caveat, assumption을 제시했는지 확인합니다.

평가 방법:

- prompt 자체가 여러 해석을 허용하는지 기록합니다.
- response가 필요한 질문을 되물었는지 확인합니다.
- 무리하게 단정하지 않았는지 확인합니다.
- 가정이 있다면 response가 이를 명시했는지 확인합니다.
- ambiguity 때문에 점수 판단이 어려운 경우 evaluator notes에 남깁니다.

애매한 prompt에서 response가 하나의 해석만 선택했더라도, 그 선택이 합리적이고 한계를 명시했다면 반드시 낮은 점수를 줄 필요는 없습니다.

## 8. How To Document Evidence

Evidence는 evaluation reproducibility를 높이는 핵심 요소입니다.

기록할 수 있는 evidence:

- response의 특정 문장 또는 표현
- prompt의 명시적 조건
- 검증 가능한 source 또는 기준 문서
- 누락된 요구사항 목록
- 위험성이 발생한 맥락
- format violation이 발생한 위치

High-stakes 영역에서는 evidence 없이 점수를 크게 낮추거나 높이지 않도록 주의합니다. 필요한 경우 external source를 확인하고 source attribution issue를 별도로 기록합니다.

## 9. Recommended Evaluation Flow

1. `data/prompt_inventory.csv`에 prompt를 등록합니다.
2. `data/response_log.csv`에 AI response를 기록합니다.
3. `rubric.md`를 기준으로 `data/evaluation_sheet.csv`에 사람이 점수를 입력합니다.
4. `scripts/validate_evaluation_data.py`로 필수 컬럼, 링크, 점수 범위를 확인합니다.
5. `scripts/calculate_scores.py`로 weighted total을 계산합니다.
6. `reports/final_analysis_report.md`에 사람이 최종 분석을 작성합니다.

이 흐름은 평가 자동화가 아니라 human review workflow를 정리하기 위한 절차입니다.
