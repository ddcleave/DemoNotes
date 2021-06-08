import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  status: "idle",
  username: ""
}

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    successAuth(state, action) {
      state.status = "true"
      state.username = action.payload
    },
    setUnauthorized(state, action) {
      state.status = "false"
      state.username = ""
    }
  }
})

export const { successAuth, setUnauthorized } = authSlice.actions

export default authSlice.reducer