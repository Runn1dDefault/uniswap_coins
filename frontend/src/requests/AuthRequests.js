import axiosInstance, {simpleRequest} from "./AxiosInstance";

export const loginRequest = async (data) =>
    await simpleRequest.post('accounts/login/', data)
        .then((data) => localStorage.setItem("jwtToken", JSON.stringify(data.data)))

export const logoutRequest = async () =>
    await axiosInstance.get('accounts/logout/')
        .then((data) => {
            localStorage.clear();
            window.location.replace("/login");
        })
