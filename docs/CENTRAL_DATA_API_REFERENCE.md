# Central Data API - Complete Reference

Complete reference documentation for the Grid.gg Central Data API (Query and Mutations API) based on the official API reference.

**API Endpoint:** `https://api-op.grid.gg/central-data/graphql`

**Authentication:** `x-api-key` header

## Table of Contents

- [Queries](#queries)
- [Mutations](#mutations)
- [Objects](#objects)
- [Inputs](#inputs)
- [Enums](#enums)
- [Interfaces](#interfaces)
- [Scalars](#scalars)

---

## Queries

### Core Entity Queries

#### `titles`
Get all titles (games).

```graphql
query Titles {
    titles(filter: TitleFilter) {
        id
        name
        nameShortened
        logoUrl
        private
    }
}
```

**Arguments:**
- `filter: TitleFilter` - Filter by title visibility

#### `title`
Get a single title by ID.

```graphql
query Title {
    title(id: "3") {
        id
        name
        nameShortened
        logoUrl
    }
}
```

**Arguments:**
- `id: ID!` - The ID of the title to retrieve

#### `tournaments`
Get multiple tournaments with filtering and pagination.

```graphql
query Tournaments {
    tournaments(
        filter: TournamentFilter
        first: Int
        after: Cursor
        last: Int
        before: Cursor
    ) {
        totalCount
        edges {
            node {
                id
                name
                nameShortened
                startDate
                endDate
            }
            cursor
        }
        pageInfo {
            hasNextPage
            hasPreviousPage
            startCursor
            endCursor
        }
    }
}
```

**Arguments:**
- `filter: TournamentFilter` - Filter specifications
- `first: Int` - Number of nodes from beginning (default: 10)
- `after: Cursor` - Cursor after which to query
- `last: Int` - Number of nodes from end
- `before: Cursor` - Cursor before which to query

#### `tournament`
Get a single tournament by ID.

```graphql
query Tournament {
    tournament(id: "756907") {
        id
        name
        nameShortened
        startDate
        endDate
        prizePool {
            amount
        }
        teams {
            id
            name
        }
        titles {
            id
            name
        }
    }
}
```

**Arguments:**
- `id: ID!` - The ID of the tournament to retrieve

#### `allSeries`
Get multiple series with filtering and pagination.

```graphql
query AllSeries {
    allSeries(
        filter: SeriesFilter
        orderBy: SeriesOrderBy!
        orderDirection: OrderDirection!
        first: Int
        after: Cursor
        last: Int
        before: Cursor
    ) {
        totalCount
        edges {
            node {
                id
                startTimeScheduled
                format {
                    name
                    nameShortened
                }
                teams {
                    baseInfo {
                        id
                        name
                    }
                }
            }
            cursor
        }
        pageInfo {
            hasNextPage
            hasPreviousPage
            startCursor
            endCursor
        }
    }
}
```

**Arguments:**
- `filter: SeriesFilter` - Filter specifications
- `orderBy: SeriesOrderBy!` - Field to order by (ID, StartTimeScheduled, UpdatedAt)
- `orderDirection: OrderDirection!` - ASC or DESC
- `first: Int` - Number of nodes from beginning (default: 10)
- `after: Cursor` - Cursor after which to query
- `last: Int` - Number of nodes from end
- `before: Cursor` - Cursor before which to query

#### `series`
Get a single series by ID.

```graphql
query Series {
    series(id: "2616372") {
        id
        startTimeScheduled
        format {
            name
            nameShortened
        }
        title {
            id
            name
        }
        tournament {
            id
            name
        }
        teams {
            baseInfo {
                id
                name
            }
            scoreAdvantage
        }
        players {
            id
            nickname
        }
    }
}
```

**Arguments:**
- `id: ID!` - The ID of the series to retrieve

#### `teams`
Get multiple teams with filtering and pagination.

```graphql
query Teams {
    teams(
        filter: TeamFilter
        first: Int
        after: Cursor
        last: Int
        before: Cursor
    ) {
        totalCount
        edges {
            node {
                id
                name
                nameShortened
                logoUrl
                colorPrimary
                colorSecondary
            }
            cursor
        }
        pageInfo {
            hasNextPage
            hasPreviousPage
        }
    }
}
```

**Arguments:**
- `filter: TeamFilter` - Filter specifications
- `first: Int` - Number of nodes from beginning (default: 10)
- `after: Cursor` - Cursor after which to query
- `last: Int` - Number of nodes from end
- `before: Cursor` - Cursor before which to query

#### `team`
Get a single team by ID.

```graphql
query Team {
    team(id: "47494") {
        id
        name
        nameShortened
        logoUrl
        colorPrimary
        colorSecondary
        title {
            id
            name
        }
        organization {
            id
            name
        }
    }
}
```

**Arguments:**
- `id: ID!` - The ID of the team to retrieve

#### `players`
Get multiple players with filtering and pagination.

```graphql
query Players {
    players(
        filter: PlayerFilter
        first: Int
        after: Cursor
        last: Int
        before: Cursor
    ) {
        totalCount
        edges {
            node {
                id
                nickname
                fullName
                age
                nationality {
                    code
                    name
                }
                team {
                    id
                    name
                }
                roles {
                    id
                    name
                }
            }
            cursor
        }
        pageInfo {
            hasNextPage
            hasPreviousPage
        }
    }
}
```

**Arguments:**
- `filter: PlayerFilter` - Filter specifications
- `first: Int` - Number of nodes from beginning (default: 10)
- `after: Cursor` - Cursor after which to query
- `last: Int` - Number of nodes from end
- `before: Cursor` - Cursor before which to query

#### `player`
Get a single player by ID.

```graphql
query Player {
    player(id: "12345") {
        id
        nickname
        fullName
        age
        nationality {
            code
            name
        }
        team {
            id
            name
        }
        title {
            id
            name
        }
        roles {
            id
            name
        }
        externalLinks {
            dataProvider {
                name
            }
            externalEntity {
                id
            }
        }
    }
}
```

**Arguments:**
- `id: ID!` - The ID of the player to retrieve

#### `organizations`
Get multiple organizations with filtering and pagination.

```graphql
query Organizations {
    organizations(
        filter: OrganizationFilter
        first: Int
        after: Cursor
        last: Int
        before: Cursor
    ) {
        totalCount
        edges {
            node {
                id
                name
                teams {
                    id
                    name
                }
            }
            cursor
        }
        pageInfo {
            hasNextPage
            hasPreviousPage
        }
    }
}
```

**Arguments:**
- `filter: OrganizationFilter` - Filter specifications
- `first: Int` - Number of nodes from beginning (default: 10)
- `after: Cursor` - Cursor after which to query
- `last: Int` - Number of nodes from end
- `before: Cursor` - Cursor before which to query

#### `organization`
Get a single organization by ID.

```graphql
query Organization {
    organization(id: "123") {
        id
        name
        teams {
            id
            name
        }
    }
}
```

**Arguments:**
- `id: ID!` - The ID of the organization to retrieve

#### `playerRoles`
Get multiple player roles.

```graphql
query PlayerRoles {
    playerRoles(filter: PlayerRoleFilter) {
        id
        name
        title {
            id
            name
        }
    }
}
```

**Arguments:**
- `filter: PlayerRoleFilter` - Filter specifications

#### `playerRole`
Get a single player role by ID.

```graphql
query PlayerRole {
    playerRole(id: "123") {
        id
        name
        title {
            id
            name
        }
    }
}
```

**Arguments:**
- `id: ID!` - The ID of the player role

#### `seriesFormats`
Get supported series formats.

```graphql
query SeriesFormats {
    seriesFormats {
        id
        name
        nameShortened
    }
}
```

**No arguments.**

### Lookup Queries

#### `seriesIdByExternalId`
Get GRID Series ID by external ID.

```graphql
query SeriesIdByExternalId {
    seriesIdByExternalId(
        dataProviderName: "STEAM"
        externalSeriesId: "external-id-123"
    )
}
```

**Arguments:**
- `dataProviderName: String!` - Data provider name (e.g., "STEAM")
- `externalSeriesId: ID!` - External series ID

#### `tournamentIdByExternalId`
Get GRID Tournament ID by external ID.

```graphql
query TournamentIdByExternalId {
    tournamentIdByExternalId(
        dataProviderName: "STEAM"
        externalTournamentId: "external-id-123"
    )
}
```

**Arguments:**
- `dataProviderName: String!` - Data provider name
- `externalTournamentId: ID!` - External tournament ID

#### `teamIdByExternalId`
Get GRID Team ID by external ID.

```graphql
query TeamIdByExternalId {
    teamIdByExternalId(
        dataProviderName: "STEAM"
        externalTeamId: "external-id-123"
        titleId: "3"
    )
}
```

**Arguments:**
- `dataProviderName: String!` - Data provider name
- `externalTeamId: ID!` - External team ID
- `titleId: ID!` - Title ID the team participates in

#### `playerIdByExternalId`
Get GRID Player ID by external ID.

```graphql
query PlayerIdByExternalId {
    playerIdByExternalId(
        dataProviderName: "STEAM"
        externalPlayerId: "external-id-123"
        titleId: ID
    )
}
```

**Arguments:**
- `dataProviderName: String!` - Data provider name
- `externalPlayerId: ID!` - External player ID
- `titleId: ID` - Optional title ID

#### `gameIdByExternalId`
Get GRID Game ID by external ID.

```graphql
query GameIdByExternalId {
    gameIdByExternalId(
        dataProviderName: "STEAM"
        externalGameId: "external-id-123"
    )
}
```

**Arguments:**
- `dataProviderName: String!` - Data provider name
- `externalGameId: ID!` - External game ID

#### `dataProviders`
Get supported data providers.

```graphql
query DataProviders {
    dataProviders {
        name
        description
    }
}
```

**No arguments.**

### Content Catalog Queries

#### `contentCatalogVersions`
Get multiple content catalog versions.

```graphql
query ContentCatalogVersions {
    contentCatalogVersions(
        filter: ContentCatalogVersionFilter
        first: Int
        after: Cursor
        last: Int
        before: Cursor
        orderBy: [ContentCatalogVersionOrder!]
    ) {
        totalCount
        edges {
            node {
                id
                name
                publishedOn
                title {
                    id
                    name
                }
            }
            cursor
        }
        pageInfo {
            hasNextPage
            hasPreviousPage
        }
    }
}
```

#### `contentCatalogVersion`
Get a single content catalog version by ID.

```graphql
query ContentCatalogVersion {
    contentCatalogVersion(id: "123") {
        id
        name
        publishedOn
        title {
            id
            name
        }
    }
}
```

#### `contentCatalogEntities`
Get multiple content catalog entities (characters, items, maps).

```graphql
query ContentCatalogEntities {
    contentCatalogEntities(
        contentCatalogVersionId: ID
        filter: ContentCatalogEntityFilter
        first: Int
        after: Cursor
        last: Int
        before: Cursor
    ) {
        totalCount
        edges {
            node {
                id
                name
                imageUrl
                ... on ContentCatalogCharacter {
                    contentCatalogVersion {
                        name
                    }
                }
                ... on ContentCatalogItem {
                    cost
                }
                ... on ContentCatalogMap {
                    bounds {
                        min { x y }
                        max { x y }
                    }
                }
            }
            cursor
        }
        pageInfo {
            hasNextPage
            hasPreviousPage
        }
    }
}
```

#### `contentCatalogEntity`
Get a single content catalog entity by ID.

```graphql
query ContentCatalogEntity {
    contentCatalogEntity(
        id: "123"
        contentCatalogVersionId: ID
    ) {
        id
        name
        imageUrl
    }
}
```

### Ingestion Request Queries

#### `ingestionRequests`
Get multiple ingestion requests.

```graphql
query IngestionRequests {
    ingestionRequests(
        filter: IngestionRequestFilter
        orderBy: IngestionRequestOrderBy!
        orderDirection: OrderDirection!
        first: Int
        after: Cursor
        last: Int
        before: Cursor
    ) {
        totalCount
        edges {
            node {
                id
                statusInformation {
                    status
                    reason {
                        message
                    }
                }
                createdAt
                updatedAt
            }
            cursor
        }
        pageInfo {
            hasNextPage
            hasPreviousPage
        }
    }
}
```

#### `ingestionRequest`
Get a single ingestion request by ID.

```graphql
query IngestionRequest {
    ingestionRequest(id: "123") {
        id
        statusInformation {
            status
        }
        players {
            nickname
        }
        teams {
            name
        }
        series {
            startTimeScheduled
        }
    }
}
```

---

## Mutations

### Entity Mutations

#### `createPlayer`
Create a new player.

```graphql
mutation CreatePlayer {
    createPlayer(createPlayerInput: {
        nickname: "PlayerName"
        title: { titleId: "3" }
        team: { teamId: "47494" }
        role: [{ id: "role-id" }]
        fullName: "Full Name"
        nationality: [{ nationalityCode: "USA" }]
        externalLinks: [{
            dataProviderName: "STEAM"
            externalEntityInput: { id: "external-id" }
        }]
    }) {
        createdPlayer {
            id
            nickname
        }
    }
}
```

#### `updatePlayer`
Update an existing player.

```graphql
mutation UpdatePlayer {
    updatePlayer(updatePlayerInput: {
        id: "12345"
        nickname: "NewNickname"
        team: { teamId: "47494" }
    }) {
        updatedPlayer {
            id
            nickname
        }
    }
}
```

#### `deletePlayer`
Delete a player.

```graphql
mutation DeletePlayer {
    deletePlayer(deletePlayerInput: {
        id: "12345"
    }) {
        id
    }
}
```

#### `createTeam`
Create a new team.

```graphql
mutation CreateTeam {
    createTeam(createTeamInput: {
        name: "Team Name"
        nameShortened: "TNM"
        title: { titleId: "3" }
        colorPrimary: "#FF0000"
        colorSecondary: "#0000FF"
        externalLinks: [{
            dataProviderName: "STEAM"
            externalEntityInput: { id: "external-id" }
        }]
    }) {
        createdTeam {
            id
            name
        }
    }
}
```

#### `updateTeam`
Update an existing team.

```graphql
mutation UpdateTeam {
    updateTeam(updateTeamInput: {
        id: "47494"
        name: "New Team Name"
        colorPrimary: "#00FF00"
    }) {
        updatedTeam {
            id
            name
        }
    }
}
```

#### `deleteTeam`
Delete a team.

```graphql
mutation DeleteTeam {
    deleteTeam(deleteTeamInput: {
        id: "47494"
    }) {
        id
    }
}
```

#### `createSeries`
Create a new series.

```graphql
mutation CreateSeries {
    createSeries(createSeriesInput: {
        title: { titleId: "3" }
        tournament: { tournamentId: "756907" }
        format: { id: "format-id" }
        startTimeScheduled: "2024-01-17T08:00:00Z"
        teams: [
            { teamId: "47494", scoreAdvantage: 0 }
            { teamId: "47558", scoreAdvantage: 0 }
        ]
        players: [{ id: "12345" }]
    }) {
        createdSeries {
            id
            startTimeScheduled
        }
    }
}
```

#### `updateSeries`
Update an existing series.

```graphql
mutation UpdateSeries {
    updateSeries(updateSeriesInput: {
        id: "2616372"
        startTimeScheduled: "2024-01-17T09:00:00Z"
        teams: [
            { teamId: "47494", scoreAdvantage: 1 }
        ]
    }) {
        updatedSeries {
            id
            startTimeScheduled
        }
    }
}
```

#### `deleteSeries`
Delete a series.

```graphql
mutation DeleteSeries {
    deleteSeries(deleteSeriesInput: {
        id: "2616372"
    }) {
        id
    }
}
```

#### `createTournament`
Create a new tournament.

```graphql
mutation CreateTournament {
    createTournament(createTournamentInput: {
        name: "Tournament Name"
        nameShortened: "TN"
        startDate: { date: "2024-01-01" }
        endDate: { date: "2024-01-31" }
        titles: [{ titleId: "3" }]
        teams: [{ teamId: "47494" }]
        venueType: LAN
        prizePool: { amount: 100000.00 }
    }) {
        createdTournament {
            id
            name
        }
    }
}
```

#### `updateTournament`
Update an existing tournament.

```graphql
mutation UpdateTournament {
    updateTournament(updateTournamentInput: {
        id: "756907"
        name: "Updated Tournament Name"
        prizePool: { amount: 200000.00 }
    }) {
        updatedTournament {
            id
            name
        }
    }
}
```

#### `deleteTournament`
Delete a tournament.

```graphql
mutation DeleteTournament {
    deleteTournament(deleteTournamentInput: {
        id: "756907"
    }) {
        id
    }
}
```

#### `createPlayerRole`
Create a new player role.

```graphql
mutation CreatePlayerRole {
    createPlayerRole(createPlayerRoleInput: {
        name: "MID"
        title: { titleId: "3" }
    }) {
        createdPlayerRole {
            id
            name
        }
    }
}
```

#### `updatePlayerRole`
Update a player role.

```graphql
mutation UpdatePlayerRole {
    updatePlayerRole(updatePlayerRoleInput: {
        id: "123"
        name: "MIDLANE"
    }) {
        updatedPlayerRole {
            id
            name
        }
    }
}
```

#### `deletePlayerRole`
Delete a player role.

```graphql
mutation DeletePlayerRole {
    deletePlayerRole(deletePlayerRoleInput: {
        id: "123"
    }) {
        deletedPlayerRole
    }
}
```

### Content Catalog Mutations

#### `createContentCatalogVersion`
Create a new content catalog version.

```graphql
mutation CreateContentCatalogVersion {
    createContentCatalogVersion(createContentCatalogVersionInput: {
        name: "7.34"
        titleId: "3"
        publishedOn: "2024-01-01T00:00:00Z"
        externalLinks: [{
            dataProviderName: "STEAM"
            externalEntityInput: { id: "external-id" }
        }]
    }) {
        createdContentCatalogVersion {
            id
            name
        }
    }
}
```

#### `createContentCatalogCharacter`
Create a content catalog character.

```graphql
mutation CreateContentCatalogCharacter {
    createContentCatalogCharacter(createContentCatalogCharacterInput: {
        contentCatalogVersionId: "123"
        name: "Champion Name"
        imageData: "base64-encoded-image"
        externalLinks: [{
            dataProviderName: "STEAM"
            externalEntityInput: { id: "external-id" }
        }]
    }) {
        createdContentCatalogCharacter {
            id
            name
        }
    }
}
```

#### `createContentCatalogItem`
Create a content catalog item.

```graphql
mutation CreateContentCatalogItem {
    createContentCatalogItem(createContentCatalogItemInput: {
        contentCatalogVersionId: "123"
        name: "Item Name"
        cost: 3500.0
        imageData: "base64-encoded-image"
    }) {
        createdContentCatalogItem {
            id
            name
            cost
        }
    }
}
```

#### `createContentCatalogMap`
Create a content catalog map.

```graphql
mutation CreateContentCatalogMap {
    createContentCatalogMap(createContentCatalogMapInput: {
        contentCatalogVersionId: "123"
        name: "Map Name"
        bounds: {
            min: { x: 0.0, y: 0.0 }
            max: { x: 100.0, y: 100.0 }
        }
        imageData: "base64-encoded-image"
    }) {
        createdContentCatalogMap {
            id
            name
        }
    }
}
```

#### `createIngestionRequest`
Submit an ingestion request.

```graphql
mutation CreateIngestionRequest {
    createIngestionRequest(input: {
        title: { name: "League of Legends" }
        players: [{
            nickname: "PlayerName"
            team: { name: "Team Name" }
        }]
        series: [{
            startTimeScheduled: "2024-01-17T08:00:00Z"
            format: { nameShortened: "Bo3" }
            teams: [{ name: "Team1" }, { name: "Team2" }]
            tournament: { name: "Tournament Name" }
        }]
    }) {
        createdIngestionRequestId
    }
}
```

---

## Objects

### Core Objects

#### `Title`
A game title.

**Fields:**
- `id: ID!` - Title ID
- `name: String!` - Title name
- `nameShortened: String!` - Shortened name (max 20 chars)
- `logoUrl: Url!` - Logo URL
- `private: Boolean` - Visibility status

#### `Tournament`
A tournament.

**Fields:**
- `id: ID!` - Tournament ID
- `name: String!` - Tournament name
- `nameShortened: String!` - Shortened name (max 30 chars)
- `startDate: Date` - Start date
- `endDate: Date` - End date
- `prizePool: Money` - Prize pool in USD
- `venueType: TournamentVenueType!` - Venue type (LAN, ONLINE, HYBRID, UNKNOWN)
- `logoUrl: Url!` - Logo URL
- `private: Boolean!` - Visibility status
- `titles: [Title!]!` - Associated titles
- `teams: [Team!]!` - Participating teams
- `children: [Tournament!]!` - Child tournaments
- `parent: Tournament` - Parent tournament
- `externalLinks: [ExternalLink!]!` - External IDs
- `updatedAt: DateTime!` - Last update time

#### `Series`
A series (match).

**Fields:**
- `id: ID!` - Series ID
- `startTimeScheduled: DateTime!` - Scheduled start time
- `format: SeriesFormat!` - Series format (Bo1, Bo3, etc.)
- `type: SeriesType!` - Series type (ESPORTS, SCRIM, COMPETITIVE, LOOPFEED)
- `title: Title!` - Game title
- `tournament: Tournament!` - Tournament
- `teams: [TeamParticipant!]!` - Participating teams
- `players: [Player!]!` - Participating players
- `streams: [VideoStream!]!` - Stream URLs
- `productServiceLevels: [ProductServiceLevel!]!` - Service levels
- `machineDataSource: MachineDataSource` - Machine data source
- `externalLinks: [ExternalLink!]!` - External IDs
- `private: Boolean!` - Visibility status
- `updatedAt: DateTime!` - Last update time

#### `Team`
A team.

**Fields:**
- `id: ID!` - Team ID
- `name: String!` - Team name
- `nameShortened: String` - Shortened name (max 20 chars)
- `logoUrl: Url!` - Logo URL
- `colorPrimary: HexColor!` - Primary color
- `colorSecondary: HexColor!` - Secondary color
- `rating: Float` - Team rating
- `title: Title!` - Associated title
- `titles: [Title!]!` - Associated titles (deprecated, use `title`)
- `organization: OrganizationRelation` - Organization
- `externalLinks: [ExternalLink!]!` - External IDs
- `private: Boolean!` - Visibility status
- `updatedAt: DateTime!` - Last update time

#### `Player`
A player.

**Fields:**
- `id: ID!` - Player ID
- `nickname: String!` - Player nickname
- `fullName: String` - Full name
- `age: Int` - Player age
- `nationality: [Nationality!]!` - Nationality
- `team: Team` - Current team
- `title: Title!` - Associated title
- `roles: [PlayerRole!]!` - Player roles
- `type: PlayerType!` - Player type (ESPORTS, REGULAR)
- `imageUrl: Url!` - Image URL
- `externalLinks: [ExternalLink!]!` - External IDs
- `private: Boolean!` - Visibility status
- `updatedAt: DateTime!` - Last update time

#### `Organization`
An organization.

**Fields:**
- `id: ID!` - Organization ID
- `name: String!` - Organization name
- `teams: [TeamRelation!]` - Associated teams
- `private: Boolean!` - Visibility status
- `updatedAt: DateTime!` - Last update time

#### `PlayerRole`
A player role.

**Fields:**
- `id: ID!` - Role ID
- `name: String!` - Role name
- `title: Title!` - Associated title
- `private: Boolean!` - Visibility status

#### `SeriesFormat`
Series format information.

**Fields:**
- `id: ID` - Format ID
- `name: String!` - Format name
- `nameShortened: String!` - Shortened name (max 5 chars)

#### `TeamParticipant`
Team participating in a series.

**Fields:**
- `baseInfo: Team!` - Team information
- `scoreAdvantage: Int!` - Score advantage

### Connection Objects

All list queries return connection objects with:
- `edges: [Edge!]!` - List of edges
- `pageInfo: PageInfo!` - Pagination info
- `totalCount: Int!` - Total count

#### `PageInfo`
Pagination information.

**Fields:**
- `hasNextPage: Boolean!` - Has next page
- `hasPreviousPage: Boolean!` - Has previous page
- `startCursor: Cursor` - First edge cursor
- `endCursor: Cursor` - Last edge cursor

### Content Catalog Objects

#### `ContentCatalogVersion`
A content catalog version.

**Fields:**
- `id: ID!` - Version ID
- `name: String!` - Version name (e.g., "7.34")
- `publishedOn: DateTime!` - Publication date
- `title: Title!` - Associated title
- `private: Boolean` - Visibility
- `externalLinks: [ExternalLink!]!` - External IDs

#### `ContentCatalogCharacter`
A character (champion) in content catalog.

**Fields:**
- `id: ID!` - Entity ID
- `name: String!` - Character name
- `imageUrl: Url!` - Image URL
- `contentCatalogVersion: ContentCatalogVersion!` - Version
- `externalLinks: [ExternalLink!]!` - External IDs
- `private: Boolean` - Visibility
- `updatedAt: DateTime!` - Last update

#### `ContentCatalogItem`
An item in content catalog.

**Fields:**
- `id: ID!` - Entity ID
- `name: String!` - Item name
- `cost: Float!` - Item cost
- `imageUrl: Url!` - Image URL
- `contentCatalogVersion: ContentCatalogVersion!` - Version
- `externalLinks: [ExternalLink!]!` - External IDs
- `private: Boolean` - Visibility
- `updatedAt: DateTime!` - Last update

#### `ContentCatalogMap`
A map in content catalog.

**Fields:**
- `id: ID!` - Entity ID
- `name: String!` - Map name
- `bounds: Bounds!` - Map boundaries
- `imageUrl: Url!` - Image URL
- `contentCatalogVersion: ContentCatalogVersion!` - Version
- `externalLinks: [ExternalLink!]!` - External IDs
- `private: Boolean` - Visibility
- `updatedAt: DateTime!` - Last update

#### `Bounds`
Map boundaries.

**Fields:**
- `min: Coordinates!` - Minimum coordinates
- `max: Coordinates!` - Maximum coordinates

#### `Coordinates`
Spatial coordinates.

**Fields:**
- `x: Float!` - X coordinate
- `y: Float!` - Y coordinate

### Other Objects

#### `Nationality`
Player nationality.

**Fields:**
- `code: String!` - ISO 3166-1 Alpha-3 code (e.g., "USA")
- `name: String!` - Country name (e.g., "United States")

#### `Money`
Monetary value.

**Fields:**
- `amount: Decimal!` - Amount in USD

#### `ExternalLink`
External entity link.

**Fields:**
- `dataProvider: DataProvider!` - Data provider
- `externalEntity: ExternalEntity!` - External entity

#### `DataProvider`
Data provider information.

**Fields:**
- `name: String!` - Provider name
- `description: String` - Description

#### `VideoStream`
Video stream information.

**Fields:**
- `url: String!` - Stream URL

#### `ProductServiceLevel`
Product service level.

**Fields:**
- `productName: String!` - Product name
- `serviceLevel: ServiceLevel!` - Service level (FULL, LIMITED, NONE)

---

## Inputs

### Filter Inputs

#### `SeriesFilter`
Filter for series.

**Fields:**
- `titleId: ID` - Filter by title ID (use `titleIds` instead)
- `titleIds: IdFilter` - Filter by title IDs
- `tournamentId: ID` - Filter by tournament ID (use `tournament` filter instead)
- `tournamentIds: IdFilter` - Filter by tournament IDs
- `tournament: SeriesTournamentFilter` - Filter by tournament
- `teamId: ID` - Filter by team ID (use `teamIds` instead)
- `teamIds: IdFilter` - Filter by team IDs
- `live: SeriesLiveFilter` - Filter by live data
- `players: SeriesPlayerFilter` - Filter by players
- `startTimeScheduled: DateTimeFilter` - Filter by start time
- `type: SeriesType` - Filter by type (use `types` instead)
- `types: [SeriesType!]` - Filter by types
- `private: BooleanFilter` - Filter by visibility
- `productServiceLevels: ProductServiceLevelFilter` - Filter by service levels
- `updatedAt: DateTimeFilter` - Filter by update time

#### `TournamentFilter`
Filter for tournaments.

**Fields:**
- `name: StringFilter` - Filter by name
- `nameShortened: StringFilter` - Filter by short name
- `startDate: NullableDateFilter` - Filter by start date
- `endDate: NullableDateFilter` - Filter by end date
- `title: TournamentTitleFilter` - Filter by titles
- `titleId: ID` - Filter by title ID (use `title` filter instead)
- `hasParent: BooleanFilter` - Has parent tournament
- `hasChildren: BooleanFilter` - Has child tournaments
- `venueType: [TournamentVenueType!]` - Filter by venue type
- `private: BooleanFilter` - Filter by visibility
- `updatedAt: DateTimeFilter` - Filter by update time

#### `TeamFilter`
Filter for teams.

**Fields:**
- `name: StringFilter` - Filter by name
- `nameShortened: StringFilter` - Filter by short name
- `titleId: ID` - Filter by title ID
- `organizationId: ID` - Filter by organization ID
- `private: BooleanFilter` - Filter by visibility
- `updatedAt: DateTimeFilter` - Filter by update time

#### `PlayerFilter`
Filter for players.

**Fields:**
- `nickname: StringFilter` - Filter by nickname
- `fullName: StringFilter` - Filter by full name
- `age: IntFilter` - Filter by age
- `nationality: NationalityFilter` - Filter by nationality
- `titleId: ID` - Filter by title ID
- `teamIdFilter: NullableIdFilter` - Filter by team ID
- `roles: PlayerPlayerRoleFilter` - Filter by roles
- `types: [PlayerType!]` - Filter by player types
- `private: BooleanFilter` - Filter by visibility
- `updatedAt: DateTimeFilter` - Filter by update time

#### `StringFilter`
String filter.

**Fields:**
- `equals: String` - Exact match (case-insensitive)
- `contains: String` - Contains string (case-insensitive)

#### `IdFilter`
ID filter.

**Fields:**
- `in: [ID!]` - Array of IDs to match

#### `IntFilter`
Integer filter.

**Fields:**
- `equals: Int` - Exact match
- `gte: Int` - Greater than or equal
- `lte: Int` - Less than or equal

#### `DateTimeFilter`
DateTime filter.

**Fields:**
- `gte: String` - Greater than or equal (ISO date string)
- `lte: String` - Less than or equal (ISO date string)

#### `BooleanFilter`
Boolean filter.

**Fields:**
- `equals: Boolean` - Exact match

---

## Enums

### `SeriesOrderBy`
Field to order series by.

- `ID` - Order by ID
- `StartTimeScheduled` - Order by scheduled start time
- `UpdatedAt` - Order by update time

### `OrderDirection`
Order direction.

- `ASC` - Ascending
- `DESC` - Descending

### `SeriesType`
Series type.

- `ESPORTS` - Esports series
- `SCRIM` - Practice series
- `COMPETITIVE` - Competitive non-esports
- `LOOPFEED` - GRID test game loop

### `PlayerType`
Player type.

- `ESPORTS` - Esports player
- `REGULAR` - Regular player

### `TournamentVenueType`
Tournament venue type.

- `LAN` - Physical location
- `ONLINE` - Online
- `HYBRID` - Both online and LAN
- `UNKNOWN` - Not specified

### `ServiceLevel`
Product service level.

- `FULL` - Fully available
- `LIMITED` - Limited functionality
- `NONE` - Not available

### `IngestionRequestStatus`
Ingestion request status.

- `PENDING` - Not yet processed
- `IN_PROGRESS` - Being processed
- `COMPLETED` - Completed successfully
- `FAILED` - Processing failed
- `REQUIRES_REVIEW` - Requires review
- `REJECTED` - Rejected by reviewer

### `IngestionRequestOrderBy`
Order field for ingestion requests.

- `ID` - Order by ID
- `CreatedOn` - Order by creation time

### `ContentCatalogEntityType`
Content catalog entity type.

- `CHARACTER` - Character
- `ITEM` - Item
- `MAP` - Map

### `ContentCatalogVersionOrderField`
Order field for content catalog versions.

- `PUBLISHED_ON` - Order by published date
- `TITLE` - Order by title name

### `ErrorType`
Error type.

- `UNKNOWN` - Unknown error
- `INTERNAL` - Internal error
- `NOT_FOUND` - Entity not found
- `UNAUTHENTICATED` - Authentication required
- `PERMISSION_DENIED` - Permission denied
- `BAD_REQUEST` - Bad request
- `UNAVAILABLE` - Service unavailable
- `FAILED_PRECONDITION` - Failed precondition

### `ErrorDetail`
Error detail.

- `UNKNOWN` - Unknown error
- `FIELD_NOT_FOUND` - Field not found
- `INVALID_ARGUMENT` - Invalid argument
- `INVALID_CURSOR` - Invalid cursor
- `DEADLINE_EXCEEDED` - Deadline exceeded
- `SERVICE_ERROR` - Service error
- `THROTTLED_CPU` - Throttled by CPU
- `THROTTLED_CONCURRENCY` - Throttled by concurrency
- `ENHANCE_YOUR_CALM` - Rate limited
- `TOO_MANY_REQUESTS` - Too many requests
- `TCP_FAILURE` - Network error
- `MISSING_RESOURCE` - Missing resource
- `UNIMPLEMENTED` - Not implemented

---

## Interfaces

### `ContentCatalogEntity`
Base interface for content catalog entities.

**Fields:**
- `id: ID!`
- `name: String!`
- `imageUrl: Url!`
- `contentCatalogVersion: ContentCatalogVersion!`
- `externalLinks: [ExternalLink!]!`
- `private: Boolean`
- `updatedAt: DateTime!`

### `OrganizationInterface`
Interface for organization types.

**Fields:**
- `id: ID!`
- `name: String!`

### `TeamInterface`
Interface for team types.

**Fields:**
- `id: ID!`
- `name: String!`
- `nameShortened: String`
- `colorPrimary: HexColor!`
- `colorSecondary: HexColor!`
- `logoUrl: Url!`
- `rating: Float`
- `titles: [Title!]!`

---

## Scalars

- `Boolean` - True/false
- `ID` - Unique identifier
- `String` - Text
- `Int` - Integer
- `Float` - Floating point number
- `Decimal` - Decimal number
- `DateTime` - ISO 8601 datetime
- `Date` - ISO 8601 date
- `Cursor` - Pagination cursor
- `Url` - URL string
- `HexColor` - Hexadecimal color (e.g., "#FF0000")

---

## Common Query Patterns

### Get Series for a Tournament

```graphql
query SeriesForTournament {
    allSeries(
        filter: {
            tournament: {
                id: { in: ["756907"] }
                includeChildren: { equals: true }
            }
        }
        orderBy: StartTimeScheduled
        orderDirection: ASC
        first: 50
    ) {
        totalCount
        edges {
            node {
                id
                startTimeScheduled
                format {
                    nameShortened
                }
                teams {
                    baseInfo {
                        id
                        name
                    }
                }
            }
            cursor
        }
        pageInfo {
            hasNextPage
            endCursor
        }
    }
}
```

### Get Players on a Team

```graphql
query PlayersOnTeam {
    players(
        filter: {
            teamIdFilter: { id: "47494" }
        }
        first: 10
    ) {
        edges {
            node {
                id
                nickname
                fullName
                roles {
                    name
                }
            }
        }
    }
}
```

### Get Teams in a Tournament

```graphql
query TeamsInTournament {
    tournament(id: "756907") {
        teams {
            id
            name
            logoUrl
        }
    }
}
```

### Filter Series by Date Range

```graphql
query SeriesByDate {
    allSeries(
        filter: {
            startTimeScheduled: {
                gte: "2024-01-01T00:00:00Z"
                lte: "2024-01-31T23:59:59Z"
            }
        }
        orderBy: StartTimeScheduled
        orderDirection: ASC
    ) {
        edges {
            node {
                id
                startTimeScheduled
                teams {
                    baseInfo {
                        name
                    }
                }
            }
        }
    }
}
```

---

## Error Handling

All queries and mutations can return errors in standard GraphQL format:

```json
{
  "errors": [
    {
      "message": "Error message",
      "extensions": {
        "errorType": "NOT_FOUND",
        "errorDetail": "INVALID_ARGUMENT"
      }
    }
  ],
  "data": null
}
```

Common error types:
- `UNAUTHENTICATED` - Missing or invalid API key
- `NOT_FOUND` - Entity doesn't exist
- `BAD_REQUEST` - Invalid query or arguments
- `PERMISSION_DENIED` - Insufficient permissions

---

## Pagination

All list queries support cursor-based pagination:

1. Use `first` and `after` for forward pagination
2. Use `last` and `before` for backward pagination
3. Check `pageInfo.hasNextPage` / `hasPreviousPage`
4. Use `pageInfo.endCursor` / `startCursor` for next/previous page

Example:
```graphql
# First page
query {
    allSeries(first: 10) {
        edges { node { id } }
        pageInfo {
            hasNextPage
            endCursor
        }
    }
}

# Next page
query {
    allSeries(first: 10, after: "cursor-from-previous") {
        edges { node { id } }
        pageInfo {
            hasNextPage
            endCursor
        }
    }
}
```

---

## Quick Reference

### Most Common Queries

1. **Get Titles** → `titles { id name }`
2. **Get Tournaments** → `tournaments(filter: { title: { id: { in: [...] } } })`
3. **Get Series** → `allSeries(filter: { tournament: { id: { in: [...] } } })`
4. **Get Teams** → `teams(filter: { titleId: "..." })`
5. **Get Players** → `players(filter: { teamIdFilter: { id: "..." } })`

### Most Common Filters

- **By Title:** `title: { id: { in: ["3"] } }`
- **By Tournament:** `tournament: { id: { in: [756907] } }`
- **By Team:** `teamIds: { in: ["47494"] }`
- **By Date:** `startTimeScheduled: { gte: "...", lte: "..." }`

---

This reference covers the complete Central Data API. For quickstart examples, see `API_DOCUMENTATION.md`. For workflow guidance, see `HACKATHON_API_GUIDE.md`.

