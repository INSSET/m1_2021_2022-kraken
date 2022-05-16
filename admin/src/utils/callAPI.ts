const BASE_URL = "http://0.0.0.0:5000/api/v1/";

function fetchAPI<T>(sub_URL: string, method: string): Promise<T> {
    return fetch(BASE_URL + sub_URL, {
        "method": method,
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(response.statusText);
        }
        return response.json();
    });
}

export default fetchAPI;