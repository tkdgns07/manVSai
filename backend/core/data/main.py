import csv

# CSV 파일 경로
input_file = 'AAPL/AAPL_LSTM3.csv'
output_file = 'AAPL/AAPL_LSTM3.csv'

# CSV 파일 읽기
with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    data = list(reader)

# 데이터를 아래서부터 읽어서 반전시키기
data_reversed = data[::-1]

# 반전된 데이터를 새로운 CSV 파일에 저장
with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    writer.writerows(data_reversed)

print(f"파일이 {output_file}로 저장되었습니다.")