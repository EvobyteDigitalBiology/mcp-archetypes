# 🏗️ MCP Archetypes

**A comprehensive collection of architectural patterns for building Model Context Protocol (MCP) clients and servers**

Welcome to MCP Archetypes! This repository showcases various architectural patterns, frameworks, transport mechanisms, and authentication strategies for developing robust MCP applications. Whether you're building weather services, data analysis tools, or complex AI-powered applications, these archetypes provide battle-tested foundations to accelerate your development.

Get in touch to submit ideas, comments or new patterns.

## 🚀 What's Inside


MCP Archetypes demonstrates implementations of MCP clients and servers using different frameworks, transports and authorization methods for different aspect of the MCP Specification.
The server implementations use simple, repeated functionalities like calls to the weather.gov API, as presented in the excellent [Quickstart](https://modelcontextprotocol.io/quickstart/server) guide by the MCP Authors.

The focus of this collection is how to architect MCP servers and clients for different tech stacks, auth requirements and interfaces.


### 📊 Architecture Matrix

This table is an overview of example implementations for server and client scripts presented in this repository.


| **Script** | Type | MCP Feature | Transport | Auth | Description |
|-----------|-----------|-----------|-----------|----------------|-------|
| [io_api_server.py](#weather-data-server-io_api_serverpy) | Server | Tools | STDIO | None  | MCP Tools Server Weather API |
| [io_tools_client_bedrock.py](#bedrock-ai-client-io_tools_client_bedrockpy)  | Client | Tools | STDIO | None | AWS Bedrock integration (Converse API) for MCP Tools |




## 🔧 Architecture Patterns

### 1. **Server-Side Patterns**

#### FastMCP Pattern
- **Use Case**: High-performance servers with minimal boilerplate
- **Benefits**: Built-in transport handling, automatic tool registration
- **Best For**: Production services, API integrations

#### Transport Flexibility
- **STDIO**: Perfect for local development and direct client connections
- **HTTP**: Ideal for web-based clients and microservice architectures

### 2. **Client-Side Patterns**

#### AI-Enhanced Client Pattern
- **Use Case**: Natural language interfaces to technical tools
- **Benefits**: User-friendly interaction, intelligent parameter inference
- **Components**: LLM integration, tool schema translation, conversation management

#### Authentication Strategies
- **AWS Bedrock**: Enterprise-grade AI with managed authentication
- **Environment Variables**: Secure credential management
- **Token-based**: Scalable authentication for distributed systems

### 3. **Transport Patterns**

#### STDIO Transport
```python
# Server setup
mcp.run(transport='stdio')

# Client connection
server_params = StdioServerParameters(
    command='python3',
    args=[server_script_path, 'local']
)
```

#### HTTP Transport
```python
# Server setup
mcp.run(transport='http')

# Client connection (future archetype)
# HTTP client implementation coming soon
```

## Use Cases & Extensions

### Current Implementations
- **Weather Services**: Real-time meteorological data
- **AI Chat Interfaces**: Natural language tool interaction

### Potential Extensions
- **Database Connectors**: PostgreSQL, MongoDB, Redis
- **API Gateways**: REST, GraphQL, gRPC services
- **File Operations**: Document processing, data transformation
- **Development Tools**: Code analysis, testing, deployment


## 🌟 Details

### Weather Data Server (`io_api_server.py`)
A production-ready MCP server that provides comprehensive weather information using the National Weather Service API.

**🎯Features:**
- **FastMCP Framework**: Lightning-fast server implementation
- **Real-time Weather Data**: Current conditions and forecasts
- **Alert System**: Weather warnings and advisories
- **Dual Transport**: Supports both STDIO and HTTP transports
- **Error Handling**: Robust error management for external API calls

**🔧Tools Provided:**
- `get_alerts(state)` - Retrieve active weather alerts for any US state
- `get_forecast(latitude, longitude)` - Get detailed weather forecasts for specific coordinates

**Transport**
- Local I/O Transport

**🛡️Required Auth & Credentials**
- None


### Bedrock AI Client (`io_tools_client_bedrock.py`)
An intelligent MCP client that leverages AWS Bedrock's powerful language models to provide natural language interfaces to MCP tools.

**🎯Features:**
- **Example Function** Natural language query for weather forcast  
- **AWS Bedrock Integration**: Access to various models from AWS and external providers (e.g. Anthropic)
- **Dynamic Tool Calling**: Automatically invokes appropriate MCP tools

**🧠 Client:**
- AWS Bedrock Runtime
- Bedrock Converse API (AWS [Docs](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference-call.html))
- Tool assess from AWS Converse API (AWS [Docs](https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use-inference-call.html))

**Transport**
- Local I/O Transport

**🛡️Required Auth & Credentials**
- Boto3 Client Config
    - Region
- Environment variables
    - AWS_BEARER_TOKEN_BEDROCK
    
    OR
    
    - Configured IAM Role for Service running the client

    OR
    
    - Configured AWS CLI

    OR
    
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY

    

## 🤝 Contributing

We welcome contributions! Here's how you can help expand MCP Archetypes:

1. **New Archetypes**: Add implementations for different frameworks
2. **Transport Patterns**: WebSockets, gRPC, message queues
3. **Authentication Methods**: OAuth, JWT, API keys
4. **Documentation**: Examples, tutorials, best practices

### Adding a New Archetype
1. Choose your framework/transport combination
2. Implement following the existing patterns
3. Add comprehensive documentation
4. Update the architecture matrix
5. Submit a pull request

## 📚 Resources

- [Model Context Protocol Specification](https://spec.modelcontextprotocol.io/)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [AWS Bedrock Developer Guide](https://docs.aws.amazon.com/bedrock/)
- [National Weather Service API](https://weather-gov.github.io/api/)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**🎯 Ready to build your next MCP application?** Start with these archetypes and customize them for your specific needs. The patterns demonstrated here scale from simple prototypes to production-ready systems.
