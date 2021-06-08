import { createSlice } from '@reduxjs/toolkit'


const initialState = {
  name: ''
}

const tagSlice = createSlice({
  name: 'tag',
  initialState,
  reducers: {
    setTag(state, action) {
      state.name = action.payload
    },
    resetTag(state, action) {
      return initialState
    }
  }
})

export const { setTag, resetTag } = tagSlice.actions

export default tagSlice.reducer