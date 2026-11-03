export const colors = {
    // The twelve main tokens
    sand: "#F4F1EA", // screen background
    surface: "#FDFCF9", // cards, sheets, inputs, the navigation bar
    sage: "#6E9C7C", // primary action
    sageDeep: "#4C7A5C", // sage text on light
    sageFill: "#E6EFE4", // selected, info
    forest: "#2E4636", // dark accents, active range chip
    crisisField: "#3A5A45", // crisis screens only
    ochre: "#C99A4E", // caution marker
    ochreFill: "#F3E7CF", // caution surface
    ink: "#33322E", // primary text
    muted: "#77746C", // secondary text
    border: "#E6E3DC", // card borders

    // The token sheet's supporting values
    sandWarm: "#F7F1E6", // heightened-caution screens only
    ochreBorder: "#E6D3A8",
    ochreInk: "#6B4E1E",
    disabledFill: "#DFDBD1",
    disabledInk: "#6F6B62",
    destructive: "#B57F6B", // delete, the Social series, and form errors.
    divider: "#D4CFC4",
    crisisBody: "#DCE7DB", // body text on crisisField
    crisisTertiary: "#C2D5C3", // the 999 line on crisisField

    tertiary: "#9D9A91", // icons, chevrons, inactive navigation
    faint: "#C6C2B8", // page dots, faint glyphs
    subtle: "#EDEAE3", // muted surfaces, tracks, calendar day with no entry
    sageTrack: "#DDE5D6", // sage progress tracks
    sleepBlue: "#7E9CB8", // the Sleep series
    clayFill: "#F1E2DC", // the delete modal's icon tile
    clayInk: "#7D5344", // text on clayFill
} as const;

// Calendar fill for mood ratings 1 to 5, from the user's own rating only
export const moodScale = [
    "#F0EBDE",
    "#DCE8D8",
    "#CFE1CA",
    "#BCD4B6",
    "#9EBF96",
] as const;

export const type = {
    largeTitle: {
        fontFamily: "PlusJakartaSans",
        fontSize: 34,
        fontWeight: "700",
        letterSpacing: -0.6,
    },
    title1: {
        fontFamily: "PlusJakartaSans",
        fontSize: 28,
        fontWeight: "700",
        letterSpacing: -0.4,
    },
    title2: {
        fontFamily: "PlusJakartaSans",
        fontSize: 22,
        fontWeight: "700",
        letterSpacing: -0.2,
    },
    title3: {
        fontFamily: "PlusJakartaSans",
        fontSize: 20,
        fontWeight: "700",
    },
    reading: {
        fontFamily: "Lora",
        fontSize: 17,
        fontWeight: "400",
        lineHeight: 28.05,
    },
    headline: {
        fontFamily: "PlusJakartaSans",
        fontSize: 17,
        fontWeight: "700",
    },
    body: {
        fontFamily: "PlusJakartaSans",
        fontSize: 17,
        fontWeight: "400",
        lineHeight: 25.5,
    },
    callout: {
        fontFamily: "PlusJakartaSans",
        fontSize: 16,
        fontWeight: "400",
        lineHeight: 24.8,
    },
    subhead: {
        fontFamily: "PlusJakartaSans",
        fontSize: 15,
        fontWeight: "600",
    },
    footnote: {
        fontFamily: "PlusJakartaSans",
        fontSize: 13,
        fontWeight: "400",
    },
    caption: {
        fontFamily: "PlusJakartaSans",
        fontSize: 12,
        fontWeight: "600",
    },
    caption2: {
        fontFamily: "PlusJakartaSans",
        fontSize: 11,
        fontWeight: "600",
    },
} as const;

export const inputFont = "sans-serif";
