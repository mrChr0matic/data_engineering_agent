import http from "k6/http";
import { sleep } from "k6";

const token = "token";

export const options = {
  scenarios: {
    job_load_test: {
      executor: "shared-iterations",
      vus: 10,        
      iterations: 100 
    }
  }
};

export default function () {

  const payload = JSON.stringify({
    client_name: "load_test",
    use_case_name: "estimate_test",
    markets: []
  });

  const params = {
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
  };

  let res = http.post(
    "https://calculator-scaled-7405615748760571.11.azure.databricksapps.com/estimate",
    payload,
    params
  );

  const job = res.json("job_id");

  http.get(
    `https://calculator-scaled-7405615748760571.11.azure.databricksapps.com/status/${job}`,
    params
  );

  sleep(2);
}