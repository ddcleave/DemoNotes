import { combineReducers, configureStore, getDefaultMiddleware } from '@reduxjs/toolkit';
import notesReducer from './components/note/notesSlice'
import editnoteReducer from './components/note/editSlice'
import authReducer from './components/control/authSlice'
import tagReducer from './components/tags/tagSlice'


const combinedReducer = combineReducers({
  auth: authReducer,
  notes: notesReducer,
  editnote: editnoteReducer,
  tag: tagReducer
})

const rootReducer = (state, action) => {
  if (action.type === 'notes/resetData') {
    state = undefined
  }
  return combinedReducer(state, action)
}

export default configureStore({
  reducer: rootReducer,
  middleware: [...getDefaultMiddleware()]
})