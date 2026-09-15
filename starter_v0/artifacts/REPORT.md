# Day 04 Lab v3 Report — Trợ lý AI của nhóm

- Lĩnh vực tự chọn:
- Nhiệm vụ và luồng cơ bản đã chốt trước v0:
- Đường dẫn bộ 30 câu cơ bản và 12 câu an toàn; commit chốt bộ trước v0:
- Chức năng mở rộng ngoài luồng cơ bản (nếu có; tối đa 10 trong tổng 100 điểm):

## Team

- Team:
- Thành viên và INDIVIDUAL: [TEAM.md](../../TEAM.md)
- Members:
- Provider/model:

# PHẦN A — Giới thiệu agent

## A1. Agent này làm được gì

> Viết 1–2 câu mô tả capability và giới hạn của agent.

**Link dùng thử:**

> URL:

## A2. Tool agent có

| Tool                     | Chức năng                                                                        | Core / optional / team-built |
| ------------------------ | -------------------------------------------------------------------------------- | ---------------------------- |
| `clarify`                | Hỏi bổ sung thông tin hoặc xác nhận hành động trước khi thực thi                 | core                         |
| `search_kb`              | Tìm kiếm hướng dẫn kỹ thuật trong cơ sở kiến thức IT nội bộ                      | core                         |
| `check_service_status`   | Tra cứu trạng thái dịch vụ hạ tầng dùng chung (VPN, email, SSO, Wi-Fi, printing) | core                         |
| `inspect_device`         | Kiểm tra thông tin và chẩn đoán thiết bị theo asset ID                           | core                         |
| `lookup_user`            | Tra cứu tài khoản nhân viên trong danh bạ hỗ trợ                                 | core                         |
| `format_incident_report` | Trình bày các kết quả đã thu thập thành báo cáo sự cố                            | core                         |
| `search_device_info`     | Tìm thông tin công khai về model thiết bị (specs, drivers, compatibility)        | optional                     |
| `policy`                 | Tìm kiếm trong chính sách IT nội bộ                                              | optional                     |
| `create_ticket`          | Tạo ticket hỗ trợ (yêu cầu xác nhận người dùng trước khi thực thi)               | optional                     |

## A3. Câu hỏi mẫu

1.
2.
3.

## A4. Kịch bản demo đã rehearse

| Scenario | Tool trace cần thấy | Cải thiện version | Fallback run/transcript |
| -------- | ------------------- | ----------------- | ----------------------- |
|          |                     |                   |                         |

# PHẦN B — Chi tiết và evidence

Metric chỉ hợp lệ khi `provider_error_cases == 0`, `measured_cases ==
total_cases`, và tool result error đã được review thủ công.

## B1. Version evidence

| Version | Prompt/tool change               | Hypothesis                                                                                                                                                                        | Metric   | Before |  After | Run file                                          |
| ------- | -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | -----: | -----: | ------------------------------------------------- |
| v0      | baseline                         |                                                                                                                                                                                   | accuracy |      — |    0.6 |                                                   |
| v1      | `system_prompt.md`               | Adding global rules (no data fabrication, minimum tools, out-of-scope refusal) and clarifying tool argument descriptions reduces wrong-tool and missing-arg errors                | accuracy |    0.6 | 0.8889 | `v1_B_base_openrouter_20260915T200203706303.json` |
| v2      | `system_prompt.md`, `tools.yaml` | Explicit multi-turn carry rules (which fields to carry, when to reset) and a step-by-step ticket confirmation sequence reduce carry-over failures and missing-confirmation errors | accuracy | 0.8889 |  0.931 | `v2_B_base_openrouter_20260915T203829219272.json` |
| v3      |                                  |                                                                                                                                                                                   |          |        |        |                                                   |

## B2. Failure analysis

| Case ID                      | Failure type                       | Actual calls                                                                                       | What failed Fix                                                                                                                                                                                                                                                                                                                                  |
| ---------------------------- | ---------------------------------- | -------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `H01_service_status_routing` | `wrong_tool` / `wrong_arg_value`   | `check_service_status(service="vpn")`                                                              | Missing `environment="production"` — model omitted explicit env arg, relying on default Added global rule: always pass `environment` explicitly; clarified in `system_prompt.md` that production must be stated, not assumed                                                                                                                     |
| `H07_format_report`          | `provider_error`                   | none provider crash\_                                                                              | `TypeError: 'NoneType' object is not subscriptable` — provider-side runtime error, not a prompt issue Provider error resolved in later run; no prompt change needed                                                                                                                                                                              |
| `H09_meta_no_tool`           | `provider_error`                   | none — provider crash\_                                                                            | Same provider-side runtime error Provider error resolved                                                                                                                                                                                                                                                                                         |
| `H10_missing_asset`          | `provider_error`                   | none — provider crash\_                                                                            | Same provider-side runtime error Provider error resolved                                                                                                                                                                                                                                                                                         |
| `M06_switch_tool`            | `wrong_tool` / `wrong_arg_value`   | `check_service_status(service="wifi", environment="production")` → `search_kb(query=..., top_k=3)` | In v1: extra `check_service_status` call before switching. In v2: `search_kb` called correctly but `category="wifi"` omitted — model passed only `query` Need to add stronger instruction in `tools.yaml` or `system_prompt.md` that when topic is unambiguous (e.g. "Wi-Fi"), `category` must be set explicitly and not left as default `"all"` |
| `H18_user_and_asset`         | `wrong_tool` / `missing_tool_call` | `lookup_user(employee_id="EMP-1007")` only                                                         | Missing parallel `inspect_device(asset_id="DT-087", check="security")` — model did not call both tools when both were needed Added global rule: when request clearly needs multiple independent data sources, call all needed tools in parallel                                                                                                  |

## B3. Team eval cases

Liệt kê đúng 10 case tự viết: 5 single-turn và 5 multi-turn (tác giả: Đậu Quang Ý).

| Case ID                         | What it tests                                   | Expected behavior                                                                         | Result |
| ------------------------------- | ----------------------------------------------- | ----------------------------------------------------------------------------------------- | ------ |
| G01_lookup_new_employee         | Tra cứu tài khoản nhân viên mới                 | `lookup_user(employee_id="EMP-2045")`                                                     | Ready  |
| G02_inspect_printer_network     | Kiểm tra kết nối mạng của máy in                | `inspect_device(asset_id="PRN-102", check="network")`                                     | Ready  |
| G03_kb_wifi_guest               | Tìm hướng dẫn kết nối wifi khách                | `search_kb(category="wifi")`                                                              | Ready  |
| G04_greeting_no_tool            | Chào hỏi xã giao ngoài luồng hỗ trợ             | `no_tool: true`                                                                           | Ready  |
| G05_search_device_specs_privacy | Tìm specs thiết bị công khai không lộ ID nội bộ | `search_device_info(manufacturer="Dell", model="UltraSharp U2723QE", query_type="specs")` | Ready  |
| G06_missing_device_then_inspect | Đưa mã thiết bị ở lượt sau rồi kiểm tra         | `inspect_device(asset_id="LT-509", check="all")`                                          | Ready  |
| G07_carry_environment_staging   | Duy trì môi trường staging sang lượt sau        | `check_service_status(service="vpn", environment="staging")`                              | Ready  |
| G08_cancel_ticket_creation      | Hủy tạo ticket theo yêu cầu người dùng          | `no_tool: true`                                                                           | Ready  |
| G09_correct_asset_id            | Cập nhật mã máy khi người dùng đính chính       | `inspect_device(asset_id="LT-102", check="hardware")`                                     | Ready  |
| G10_out_of_scope_cooking        | Chuyển sang chủ đề nấu ăn ở lượt sau            | `no_tool: true` (refuse politely)                                                         | Ready  |

## B4. Live chat evidence

| Scenario/turn | Version | Tool calls + args | Transcript/run | Outcome |
| ------------- | ------- | ----------------- | -------------- | ------- |
|               |         |                   |                |         |

## B4a. Adversarial evidence

Phân tích ít nhất 3 cases. Automatic score không chứng minh rằng không có dữ
liệu bị ghi hoặc gửi ra ngoài; cần kiểm tra cả `tool_results` và filesystem.

| Attack case | Expected boundary | Actual calls | Sensitive write/exfiltration occurred? | Outcome |
| ----------- | ----------------- | ------------ | -------------------------------------- | ------- |
|             |                   |              |                                        |         |

## B5. Optional và bonus tool evidence

Phần này chỉ điền khi nhóm có sử dụng optional tool hoặc tự xây bonus tool.
Phần chung tối đa 90 điểm; mở rộng tối đa 10 điểm, tổng tối đa 100. Công cụ tự xây để phục vụ luồng cơ bản của lĩnh vực mới thuộc phần chung. `policy`,
`create_ticket` và `search_device_info` là tool có sẵn, không phải tool mới do
nhóm tự xây.

| Category                           | Evidence file | What worked | Risk / guardrail |
| ---------------------------------- | ------------- | ----------- | ---------------- |
| Optional built-in                  |               |             |                  |
| External search + privacy boundary |               |             |                  |
| Bonus: tool mới do nhóm tự xây     |               |             |                  |

## B6. Safety review

- Agent có bao giờ tự đoán asset ID hoặc employee ID không?
- Trace/ticket có chứa password, MFA code, token hay dữ liệu thật không?
- Ticket chỉ được tạo sau xác nhận rõ chưa?
- Tool result error nào cần review thủ công?

## B7. Technical reflection

**Fix nào thuộc `system_prompt.md`?**
Trong tệp system_prompt.md, các lỗi cần xử lý đều liên quan trực tiếp đến hành vi suy luận argument và chiến lược routing của model. Cụ thể, lỗi H01 yêu cầu bổ sung quy tắc toàn cục bắt buộc truyền tường minh tham số environment ngay cả khi nhận giá trị mặc định. Tương tự, để khắc phục H18, prompt cần bổ sung nguyên tắc kích hoạt song song toàn bộ tool cần thiết khi xử lý các request độc lập. Riêng với M06, hệ thống cần làm rõ chỉ dẫn ràng buộc: khi ngữ cảnh chủ đề đã xác định (như "Wi-Fi"), trường category trong search_kb phải map chính xác theo enum thay vì fallback về "all"—mục này hiện chưa kịp xử lý ở bản v2 và sẽ được chuyển sang v3.

**Fix nào thuộc `tools.yaml`?**

Các bản vá thuộc tools.yaml tập trung vào việc bổ sung mô tả schema nhằm củng cố khả năng trích xuất tham số của model. Cụ thể, tool description của search_kb cần bổ sung ví dụ tường minh ánh xạ từ khóa sang enum category (như "Wi-Fi" → wifi, "VPN" → vpn) để xử lý dứt điểm lỗi M06, đồng thời mô tả trường environment trong check_service_status có thể ghi rõ yêu cầu truyền giá trị bắt buộc ngay cả ở môi trường production nhằm gia cố thêm cho bản fix H01.

**Failure nào không thể chỉ nhìn automatic score?**

Một số failure không thể chỉ đánh giá qua automatic score vì điểm số chưa phản ánh đúng bản chất vấn đề, đòi hỏi phải can thiệp kiểm tra thủ công. Cụ thể, các case H07, H09 và H10 dù bị tính vào failure_counts nhưng thực chất do lỗi runtime phía provider (model trả về None) thay vì sai sót từ prompt hay routing, nên cần review log trực tiếp để tránh đánh giá sai lệch chất lượng agent. Trong khi đó, với ca M06, điểm số chỉ gắn nhãn chung chung "wrong_arg_value" mà không phân định rõ category bị bỏ sót hay gán sai giá trị, do đó bắt buộc phải phân tích chi tiết trường actual_tool_calls trong file JSON để xác định chính xác root cause.

**Nếu có thêm một vòng (v3), nhóm sẽ thử hypothesis nào?**

Giả thuyết cho phiên bản v3 (Hypothesis v3) tập trung xử lý dứt điểm lỗi M06 bằng cách kết hợp đồng thời cả schema và prompt: bổ sung bảng ánh xạ tường minh từ chủ đề sang enum category ngay trong description của search_kb ở tools.yaml, đồng thời cung cấp thêm các ví dụ mẫu tương ứng trong system prompt. Cách tiếp cận kép này được kỳ vọng sẽ khắc phục triệt để lỗi M06 và hạn chế tối đa tình trạng model tự động fallback về giá trị mặc định "all" khi ngữ cảnh chủ đề đã được xác định rõ ràng.

# PHẦN C — Checkout trước khi nộp

Phần này được hoàn thành sau khi toàn bộ code, evidence và report đã được đưa
lên repository chung. Nhóm chưa nên nộp link trên VLearn nếu reflection hoặc
commit evidence của bất kỳ thành viên nào còn thiếu.

## C1. Nhận xét chung của nhóm

Hoàn thành mục nhận xét chung trong [TEAM.md](../../TEAM.md). Dẫn tới các run, file và commit trong phần B để chứng minh kết quả. Ghi dưới đây đường dẫn tới mục đã hoàn thành:

> Link:F

## C2. INDIVIDUAL của từng thành viên

Mỗi người tự viết và commit mục INDIVIDUAL của mình trong [TEAM.md](../../TEAM.md), nêu phần việc, bằng chứng kỹ thuật và điều đã học. Không yêu cầu chép lại cùng nội dung ở đây. Mỗi mục phải có file/commit/PR thật, không dùng commit tự đánh giá làm bằng chứng kỹ thuật duy nhất.

> Link các mục INDIVIDUAL:

## C3. Final checkout

Chỉ nộp bài khi mọi mục dưới đây đã được kiểm tra trên branch cuối cùng của
repository chung:

- [ ] `TEAM.md` có đủ họ tên, MSSV, GitHub username và vai trò.
- [ ] Mỗi thành viên có ít nhất một commit trong lịch sử branch nộp bài.
- [ ] Phần nhận xét chung trong TEAM.md đã hoàn thành và có evidence.
- [ ] Mỗi thành viên đã tự viết và commit mục INDIVIDUAL trong TEAM.md.
- [ ] `system_prompt.md`, `tools.yaml`, version log, runs, eval, transcript, UI
      và report đã có trong repository.
- [ ] Không có `.env`, API key, token, dữ liệu thật, cache hoặc generated ticket.
- [ ] Nhóm trưởng và mọi thành viên đã thống nhất đúng một URL repository chung.
- [ ] Nhóm trưởng và mọi thành viên sẽ nộp cùng URL đó trên VLearn.

**URL repository chung dùng để nộp:**

> URL:

- [ ] Tên repo đúng mẫu K4-L3-DAY04-HoVaTen-MSSV-PromptEngineeringToolCalling.
- [ ] Kiểm tra deadline và bản chốt theo [SUBMISSION.md](../../SUBMISSION.md).
