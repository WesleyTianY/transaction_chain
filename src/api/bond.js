import axios from 'axios';
import config from '../config';

const baseURL = config[process.env.NODE_ENV].baseURL;

async function fetchBondData(displayInfo) {
  const response = await axios.get(`${baseURL}/api/bondData`, {
    params: {
      BondId: displayInfo.bondId,
      selectedDate: displayInfo.date
    }
  });
  return response

}


async function fetchBondSummaryData(queryDate) {
  const response = await axios.get(`${baseURL}/api/bondSummaryData`,{
    params: {
      date: queryDate
    }
  });
  return response.data.bondSummaryData;

}

async function fetchBondSummaryData_ByBond_cd(Bond_cd) {
  const response = await axios.get(`${baseURL}/api/bondSummaryData_ByBond_cd/${Bond_cd}`,{
    params: {
      Bondcd: Bond_cd,
    }
  });
  return response.data.bondSummaryData;

}

export { fetchBondSummaryData, fetchBondSummaryData_ByBond_cd, fetchBondData};
