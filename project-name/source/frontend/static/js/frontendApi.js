class FrontendApi {
  constructor(apiUrl) {
    this.apiUrl = apiUrl;
  }

  /**
   * Get profile data for a given username.
   * @param {string} username - The username.
   * @returns {Promise<Object>} The profile data.
   * @throws {Error} If the request fails or returns an error response.
   */
  async getProfileData(username) {
    try {
      const response = await fetch(`${this.apiUrl}/api/profile/${username}`);
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error);
      }
      const data = await response.json();
      return data;
    } catch (error) {
      console.error(error);
      throw new Error('Failed to fetch profile data');
    }
  }

  /**
   * Update user status.
   * @param {string} status - The new user status.
   * @returns {Promise<Object>} The updated status object.
   * @throws {Error} If the request fails or returns an error response.
   */
  async updateStatus(status) {
    try {
      const response = await fetch(`${this.apiUrl}/api/status`, {
        method: 'POST',
        body: JSON.stringify({ status }),
        headers: {
          'Content-Type': 'application/json',
        },
      });
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error);
      }
      const data = await response.json();
      return data;
    } catch (error) {
      console.error(error);
      throw new Error('Failed to update status');
    }
  }

  /**
   * Get gifters list.
   * @returns {Promise<Object>} The list of gifters.
   * @throws {Error} If the request fails or returns an error response.
   */
  async getGiftersList() {
    try {
      const response = await fetch(`${this.apiUrl}/api/gifters`);
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error);
      }
      const data = await response.json();
      return data;
    } catch (error) {
      console.error(error);
      throw new Error('Failed to fetch gifters');
    }
  }

  /**
   * Wave at a user.
   * @param {string} username - The username to wave at.
   * @returns {Promise<Object>} The result of waving.
   * @throws {Error} If the request fails or returns an error response.
   */
  async wave(username) {
    try {
      const response = await fetch(`${this.apiUrl}/api/wave`, {
        method: 'POST',
        body: JSON.stringify({ username }),
        headers: {
          'Content-Type': 'application/json',
        },
      });
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error);
      }
      const data = await response.json();
      return data;
    } catch (error) {
      console.error(error);
      throw new Error('Failed to wave');
    }
  }

  /**
   * Gift sushi to the user.
   * @returns {Promise<Object>} The result of gifting sushi.
   * @throws {Error} If the request fails or returns an error response.
   */
  async giftSushi() {
    try {
      const response = await fetch(`${this.apiUrl}/api/gift`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error);
      }
      const data = await response.json();
      return data;
    } catch (error) {
      console.error(error);
      throw new Error('Failed to gift sushi');
    }
  }

  /**
   * Get sushi gifters list.
   * @returns {Promise<Object>} The list of sushi gifters.
   * @throws {Error} If the request fails or returns an error response.
   */
  async getSushiGiftersList() {
    try {
      const response = await fetch(`${this.apiUrl}/api/sushi-gifters`);
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error);
      }
      const data = await response.json();
      return data;
    } catch (error) {
      console.error(error);
      throw new Error('Failed to fetch sushi gifters');
    }
  }
}