import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  // 1. หําไฟล์ dictionary อังกฤษ >20,000 คำ ท ําเป็น text file 

  // 2. เอามาสร้างไฟล์ text โดยให้ชื่อไฟล์เป็นชื่อคำศัพท์ เช่น joke --> joke.txt โดยในเนื้อหําไฟล์เป็นคำ ๆ นั้น (เปิดไฟล์ joke.txt เจอคำว่ํา joke ในไฟล์ โดยให้มีซ้ำ ๆ ไป 100 ครั้ง)
  

  return (
    <>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
      </div>
    </>
  )
}

export default App
