import ReactTable from "react-table"
import React, { Component } from 'react'
import 'react-table/react-table.css'

class App extends Component {
  state = {}

  async componentDidMount() {
    try {
      this.interval = setInterval(async () => {
        const res = await fetch('http://127.0.0.1:8080/all')
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

  async removeWatcher(watcher) {
    const res = await fetch('http://127.0.0.1:8080/watcher/'+watcher, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    const j = await res.json()
    console.log(j)
  }

  render() {
    const columns = [{
      Header: 'Name',
      accessor: 'name'
    }, {
      Header: 'Command',
      accessor: 'cmd'
    }, {
      Header: 'Arguments',
      accessor: 'args'
    }, {
      Header: 'Status',
      accessor: 'status'
    }, {
      Header: 'PIDs',
      accessor: 'pids'
    }, {
      Header: 'Controls',
      accessor: 'name',
      Cell: ({value}) => (
        <button onClick={() => this.removeWatcher(value)}>Remove</button>
      )
    }]
    return (
      <div className="App">
        <ReactTable
          data={this.state.watchers}
          columns={columns}
        />
      </div>
    )
  }
}

export default App
