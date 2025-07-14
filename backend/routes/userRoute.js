import express from "express";
import {
  loginUser,
  registerUser,
  loginAdmin,
  getUserInfo,
} from "../controllers/userController.js";

const userRouter = express.Router();

userRouter.post("/register", registerUser);
userRouter.post("/login", loginUser);
userRouter.post("/admin", loginAdmin);
userRouter.post("/info", getUserInfo);

export default userRouter;
