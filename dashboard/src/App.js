import React, { Component, Fragment } from 'react'
import ReactTable from "react-table"
import 'react-table/react-table.css'
import './App.css'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faSyncAlt, faPlay, faPause, faTimes } from '@fortawesome/free-solid-svg-icons'

const ENDPOINT = 'http://127.0.0.1:8080'

class App extends Component {
  state = {}

  async updateFromApi() {
    const res = await fetch(ENDPOINT + '/all')
    const watchers = await res.json()
    this.setState({
      watchers: watchers,
    })
  }

  async componentDidMount() {
    try {
      this.interval = setInterval(async () => {
        this.updateFromApi()
      }, 1000)
    } catch(e) {
      console.log(e)
    }
  }

  componentWillUnmount() {
    clearInterval(this.interval)
  }

  async fetchApi(loc, opts = {}) {
    const req = await fetch(loc, opts)
    const res = await req
    this.updateFromApi()
    console.debug(loc, await res.json())
  }

  async removeWatcher(watcher) {
    await this.fetchApi(ENDPOINT + '/watcher/' + watcher, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json'
      }
    })
  }

  async restartWatcher(watcher) {
    await this.fetchApi(ENDPOINT + '/watcher/restart/' + watcher, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })
  }

  async startWatcher(watcher) {
    await this.fetchApi(ENDPOINT + '/watcher/start/' + watcher, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })
  }

  async stopWatcher(watcher) {
    await this.fetchApi(ENDPOINT + '/watcher/stop/' + watcher, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })
  }

  render() {
    const columns = [{
      Header: 'Process monitor',
      columns: [{
        Header: 'Name',
        accessor: 'name'
      }, {
        Header: 'Command',
        accessor: 'cmd',
        Cell: row => (
          <span>
            {row.row.name}{' '}{row.row._original.args.join(" ")}
          </span>
        )
      }, {
        Header: 'Status',
        accessor: 'status',
        className: 'center',
        Cell: row => (
          <span>
            <span className={row.value}>&#x25cf;</span> {row.value}
          </span>
        )
      }, {
        Header: 'PID',
        accessor: 'pids',
        className: 'center'
      }, {
        Header: 'Controls',
        accessor: 'name',
        className: 'center',
        Cell: row => (
          <Fragment>
            {row.row.status === 'stopped' && <FontAwesomeIcon className="icon play" onClick={() => this.startWatcher(row.row.name)} icon={faPlay} />}
            {row.row.status === 'active' && <FontAwesomeIcon className="icon pause" onClick={() => this.stopWatcher(row.row.name)} icon={faPause} />}
            <FontAwesomeIcon className="icon reload" onClick={() => this.restartWatcher(row.row.name)} icon={faSyncAlt} />
            <FontAwesomeIcon className="icon remove" onClick={() => this.removeWatcher(row.row.name)} icon={faTimes} />
          </Fragment>
        )
      }]
    }]
    return (
      <div className="App">
        <ReactTable
          data={this.state.watchers}
          noDataText="No process"
          columns={columns}
          collapseOnDataChange={false}
          SubComponent={row => (
            <div className="rowAdditional">
              <em>More informations</em><br /><br />
              {JSON.stringify(row.row._original)}
            </div>
          )}
        />
      </div>
    )
  }
}

export default App
