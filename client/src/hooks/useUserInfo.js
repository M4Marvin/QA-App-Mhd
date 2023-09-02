import { useContext } from "react";
import { AuthContext } from "../contexts/AuthContext";

export const useUserInfo = () => {
  const { userInfo, isLoading, error } = useContext(AuthContext);

  return { userInfo, isLoading, error };
};
