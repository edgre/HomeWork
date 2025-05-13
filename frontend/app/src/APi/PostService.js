import axios from "axios";

export default class PostService {
  static async getAll(limit = 10, page = 1) {
    const response = await axios.get(URL, {
      params: {
        _limit: limit,
        _page: page,
      },
    });
    return response;
  }

  static async getById(id) {
    const response = await axios.get(URL + id);
    return response;
  }
}
