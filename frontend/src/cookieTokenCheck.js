import getCookie from './getCookie';
import apiBaseUrl from './apiBaseUrl';

export default async function cookieTokenCheck() {
    const token = getCookie('access_token');
    if(token !== "" && await tokenIsValid(token)) {
        return true;
    } else {
        return false;
    }
}

async function tokenIsValid(token) {
    let success;
    const url = apiBaseUrl + "/token";
    const params = {
        method: 'get',
        headers: {
            'Authorization': 'Bearer ' + token,
        },
    };
    const resp = await fetch(url, params);
    if(resp.status === 200) {
        success = true;
    } else {
        success = false;
    }
    return success;
}