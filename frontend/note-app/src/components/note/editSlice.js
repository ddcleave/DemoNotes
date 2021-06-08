import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  open: false,
  id: "",
  data: {}
}

const editSlice = createSlice({
  name: 'editnote',
  initialState,
  reducers: {
    openEdit(state, action) {
      const { id, data, tagged } = action.payload
      state.open = true
      state.id = id
      state.data = data
      state.tagged = tagged
    },
    closeEdit(state, action) {
      state.open = false
    },
    resetEdit(state, action) {
      return initialState
    }
  }
})

export const { openEdit, closeEdit, resetEdit } = editSlice.actions

export default editSlice.reducer