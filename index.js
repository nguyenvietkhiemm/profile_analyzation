const axios = require('axios');
const { parse } = require('json2csv');  // Import thư viện json2csv
const fs = require('fs');  // Import fs để ghi file

// set up the request parameters
const params = {
  api_key: "992B9F7440CB44C6BFC9662D6DBD8E13",
  q: '"IT" -intitle:"profiles" -inurl:"dir/ " site:vn.linkedin.com/in/ OR site:vn.linkedin.com/pub/ masters OR mba OR master OR diplome OR msc OR magister OR magisteres OR maitrise',
  location: "Vietnam",
  google_domain: "google.com.vn",
  gl: "vn",
  hl: "vi",
  num: "100"
};

const columns = ["title", "link", "domain"];

// Hàm ghi dữ liệu vào CSV
const writeToCsv = (data) => {
  const csv = parse(data, { fields: columns });
  fs.appendFileSync('python/data.csv', csv);
};

const fetchPage = async (page) => {
  try {
    params.page = page; // Cập nhật số trang
    const response = await axios.get('https://api.scaleserp.com/search', { params });
    const jsonData = response.data.organic_results;

    if (jsonData && jsonData.length > 0) {
      writeToCsv(jsonData);
      console.log(`Dữ liệu đã được ghi vào data.csv từ trang ${page}`);
    } else {
      console.log(`Không có dữ liệu từ trang ${page}`);
    }
  } catch (error) {
    console.error(`Lỗi khi lấy dữ liệu từ trang ${page}:`, error);
  }
};

// Chạy từ trang 1 đến 100
const run = async () => {
  for (let page = 1; page <= 100; page++) {
    await fetchPage(page);
  }
};

run();
