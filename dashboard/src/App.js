import React, { Component } from 'react'
import './App.css'

class App extends Component {
  state = {}

  async componentDidMount() {
    try {
      this.interval = setInterval(async () => {
        const res = await fetch('http://localhost:8080/watchers')
        const watchers = await res.json()
        this.setState({
          watchers: watchers,
        })
      }, 1000)
    } catch(e) {
      console.log(e)
    }
  }

  componentWillUnmount() {
    clearInterval(this.interval)
  }


  render() {
    console.log(this.state)
    return (
      <div className="App">
        {JSON.stringify(this.state, null, 2)}
      </div>
    )
  }
}

export default App
