import axios from 'axios';
import config from '../config';

const baseURL = config[process.env.NODE_ENV].baseURL;

export const getInstitutionTypes = async () => {
  try {
    const response = await axios.get(`${baseURL}/api/institution_types`);
    const data = JSON.parse(response.data.instn_dict);
    return data;
  } catch (error) {
    console.error('Error fetching institution types:', error);
    throw error;
  }
};
