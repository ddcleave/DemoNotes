import { createAsyncThunk, createSlice, current } from '@reduxjs/toolkit'
import wrapFunc from './components/utils/refreshToken'

const initialState = {
  status: 'idle',
  notes: [],
  full: false
}

export const getNotes = createAsyncThunk(
  'notes/getNotes',
  async (position) => {
    const url = new URL('http://localtest.me/note/notes')
    if (typeof position !== 'undefined') {
      url.search = new URLSearchParams({ "position": position })
    }
    
    // const response = await fetch(url)
    const response = await wrapFunc(async () => await fetch(url))
    const data = await response.json()
    return data
  }
)

const notesSlice = createSlice({
  name: 'notes',
  initialState,
  reducers: {
    setStatus(state, action) {
      state.status = "secceeded"
    },
    noteAdded(state, action) {
      state.notes.unshift(action.payload)
    },
    noteUpdated(state, action) {
      const { id, data } = action.payload
      const noteForUpdate = state.notes.find((note) => note.id === id)
      if (noteForUpdate) {
        noteForUpdate.note = data
      }
    },
    noteDeleted(state, action) {
      const id = action.payload
      const tmp = state.notes.filter((note) => note.id !== id)
      state.notes = tmp
    },
    notesAdded(state, action) {
      state.notes.concat(action.payload)
    }
  },
  extraReducers: {
    [getNotes.pending]: (state, action) => {
      state.status = 'loading'
    },
    [getNotes.fulfilled]: (state, action) => {
      state.status = 'secceeded'
      // state.notes = action.payload
      if (action.payload.length === 0) {
        state.full = true
      } else {
        const data = state.notes.concat(action.payload)
        state.notes = data
      }
    },
    [getNotes.rejected]: (state, action) => {
      state.status = 'failed'
    }
  }
})

export const { setStatus, noteAdded, notesAdded, noteUpdated, noteDeleted } = notesSlice.actions

export default notesSlice.reducer