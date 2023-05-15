examples = """
# Chi nhánh tại quận Đống Đa?
MATCH (b:Branch) 
WHERE b.district = "Quận Đống Đa" 
RETURN b.name + ", địa chỉ:"+  b.place
LIMIT 25

# Tiết kiệm thường lãi định kỳ có mức lãi suất và lượng tiền gửi tối thiểu là?
MATCH (s:Service), (sir:SavingInterestRate)
WHERE s.service_name = "Tiết kiệm thường lãi định kỳ" AND sir.ServiceName = "Tiết kiệm thường lãi định kỳ"
RETURN "Lãi suất là " + sir.`12months` + "% và tiến gửi tối thiểu là:" +sir.MinimumDepositAmount;  

# Mức lãi suất của gói tiết kiệm điện tử kỳ hạn 6 tháng?
MATCH (s:Service)-[:HAS_SAVING_RATE]->(sr:SavingInterestRate)
WITH s.service_name as ServiceName, max(sr.`6months`) as Max6months
RETURN "Lãi suất của gói " + ServiceName + " là: " + Max6months as Max6months
ORDER BY Max6months DESC
LIMIT 1

# Cho biết gói tiết kiệm đang có mức lãi suất cao nhất tại ngân hàng?
MATCH (sv:Service)-[:HAS_SAVING_RATE]->(s:SavingInterestRate)
WITH sv.service_name as ServiceName, max(s.`12months`) as Max12Months
RETURN ServiceName + " là gói tiết kiệm với mức lãi suất cao nhất, lãi suất kỳ hạn 12 tháng là: C" + toString(Max12Months) AS Message
ORDER BY Max12Months DESC
LIMIT 1

# Có những hạng thẻ gì tại Ngân hàng X?
MATCH (c:Card)-[r:HAS_CARD_LEVEL]->(cl:CardLevel) RETURN DISTINCT cl.CardLevelName LIMIT 25

# Cho biết hạng thẻ platinum có những loại thẻ nào?
MATCH (c:Card)-[:HAS_CARD_LEVEL]->(cl:CardLevel)
WHERE cl.CardLevelName = "Thẻ Platinum"
RETURN c.CardName AS CardName
LIMIT 25

# Những lợi ích khi mở thẻ tín dụng quốc Tế XBank Visa?
MATCH (c:Card {CardName: 'Thẻ Tín Dụng Quốc Tế XBank Visa'})-[:HAS_CARD_BENEFIT]->(cb:CardBenefit)
RETURN cb.CardBenefitDescripton AS CardBenefitDescription

# Thời gian và mức cho vay tối đa nếu vay mua xe ô tô mới?
MATCH (s:Service {service_name: "Vay mua ô tô"})-[:HAS_LOAN_RATE]->(lir:LoanInterestRate)
RETURN "Hiện nay, vay mua ô tô có thời gian vay tối đa là: " + lir.LoanPeriod + " và mức vay tối đa là: " + lir.LoanLimit AS LoanInfo

# Thủ tục đăng ký vay mua ô tô như thế nào?
MATCH (s:Service {service_name: 'Vay mua ô tô'})
RETURN s.service_register
LIMIT 1

# Số tiền tối thiểu áp dụng đối với sản phẩm tiền gửi có kỳ hạn lĩnh lãi định kỳ dành cho khách hàng doanh nghiệp?
MATCH (s:Service)-[:HAS_SAVING_RATE]->(sr:SavingInterestRate)
WITH s.service_name as ServiceName, min(sr.MinimumDepositAmount) as MinDepositAmount
RETURN "Số tiền tối thiểu đối với sản phẩm " + ServiceName + " là: " + toString(MinDepositAmount)
ORDER BY MinDepositAmount ASC
LIMIT 1

# Cho biết chi phí mở thẻ XBank Visa FreeGo tại ngân hàng mình?
MATCH (c:Card)-[r:HAS_CARD_LEVEL]->(cl:CardLevel)
WHERE c.CardName = "XBank Visa FreeGo"
RETURN r.OpenFee
LIMIT 1

# Đăng ký thẻ chính XBank Visa Gold, tôi được hưởng những quyền lợi gì?
MATCH (c:Card {CardName: 'Thẻ XBank Visa Gold'})-[:HAS_CARD_BENEFIT]->(cb:CardBenefit)
RETURN "Thẻ XBank Visa Gold cung cấp các lợi ích sau: " + REDUCE(s = "", x in COLLECT(cb.CardBenefitDescripton) | s + x + ", ") AS CardBenefitDescription
LIMIT 1

# Có chính sách bảo mật gì với thẻ và tài khoản của khách hàng?
MATCH (n:Security) 
RETURN "Khi khách hàng tạo thẻ và tài khoản ở Xbank sẽ được bảo mật về: " + REDUCE(s = "", x in COLLECT(n.SecurityName) | s + x + ", ") AS SecurityNames
LIMIT 30

# Cho biết mức lãi suất của gói Tiết kiệm điện tử kỳ hạn 6 tháng?
MATCH (s:Service)-[:HAS_SAVING_RATE]->(sr:SavingInterestRate)
WITH s.service_name as ServiceName, max(sr.`6months`) as Max6months
RETURN "Lãi suất của gói " + ServiceName + " là: " + Max6months as Max6months
ORDER BY Max6months DESC
LIMIT 1

# Có những hạng thẻ gì tại Ngân hàng X?
MATCH (c:Card)-[r:HAS_CARD_LEVEL]->(cl:CardLevel) RETURN DISTINCT cl.CardLevelName LIMIT 25

# Thời gian và mức cho vay tối đa nếu vay mua xe ô tô mới?
MATCH (s:Service {service_name: "Vay mua ô tô"})-[:HAS_LOAN_RATE]->(lir:LoanInterestRate)
RETURN "Hiện nay, vay mua ô tô có thời gian vay tối đa là: " + lir.LoanPeriod + " và mức vay tối đa là: " + lir.LoanLimit AS LoanInfo

# Ai có thể đăng ký dịch vụ tại ngân hàng? 
MATCH (a:Answer {Title: 'Đăng ký sử dụng dịch vụ'}) RETURN a.Answer

# Những lợi ích khi mở thẻ tại XBank?
MATCH (c:Card)-[:HAS_CARD_BENEFIT]->(cb:CardBenefit)
RETURN "Khi mở thẻ tại XBank, tùy từng loại thẻ và hạng thẻ, bạn có thể sẽ được hưởng những lợi ích sau: " + REDUCE(s = "", x in COLLECT(cb.CardBenefitDescripton) | s + x + ", ") AS CardBenefitDescription
LIMIT 1

# Có thể vay số tiền tối đa bao nhiêu?
MATCH (l:LoanInterestRate)
WITH toInteger(substring(l.LoanLimit, 0, size(l.LoanLimit) - 1)) AS loanLimit
RETURN loanLimit
ORDER BY loanLimit DESC
LIMIT 2

# Có thể vay tối đa trong thời gian bao lâu?
MATCH (l:LoanInterestRate)
WITH toInteger(substring(l.LoanPeriod, 0, size(l.LoanPeriod) - 6)) AS loanPeriod
RETURN loanPeriod
ORDER BY loanPeriod DESC
LIMIT 

# Giới thiệu về ngân hàng X?
MATCH (a:Answer {Title: 'Giới thiệu', AnswerType: 'Who'})
RETURN a.Answer
"""
